from flask_restx import Namespace, Resource, fields
from ..db import job_listings
from app.db import abtest
from http import HTTPStatus
from flask import request, session
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime, timedelta
from .utils import validate_email, is_valid_password  # validate emails and passwords
import uuid

authorizations = {
    "apikey": {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

def get_session_id():
    if "session_id" not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

api = Namespace("job_listings", description="Endpoint for job listings API", authorizations=authorizations)

JOB_LISTING_CREATE_FLDS = api.model(
    "AddJoblistingEntry",
    {
        job_listings.TITLE: fields.String,
        job_listings.COMPANY: fields.String,
        job_listings.LOCATION: fields.String,
        job_listings.INDUSTRY: fields.String,
        job_listings.SENIORITY: fields.String,
    },
)

JOB_LISTING_UPDATE_FLDS = api.model(
    "UpdateJobListingEntry",
    {   
        "id": fields.String(required=True, description="Unique ID in MongoDB for the current job listing"),
        job_listings.TITLE: fields.String,
        job_listings.COMPANY: fields.String,
        job_listings.LOCATION: fields.String,
        job_listings.INDUSTRY: fields.String,
        job_listings.SENIORITY: fields.String,
    },
)

JOB_LISTING_SELECT_FLDS = api.model(
    "SelectApplicantEntry",
    {   
        "id": fields.String(required=True, description="Unique ID in MongoDB for the current job listing"),
        "email": fields.String(required=True, description="Email of the applicant")
    },
)

@api.route("/")
@api.response(HTTPStatus.OK, "Success")
@api.response(HTTPStatus.NOT_FOUND, "Job Listings Not Found")
@api.response(HTTPStatus.CONFLICT, "Job listing already exists")
class JobListingList(Resource):
    @api.doc("List all job listings",
             params={
                 "company": "Filter by company name",
                 "title": "Filter by job title",
                 "location": "Filter by job location",
                 "industry": "Filter by industry",
                 "seniority": "Filter by seniority level"
             })
    
    def get(self):
        company = request.args.get(job_listings.COMPANY)
        title = request.args.get(job_listings.TITLE)
        location = request.args.get(job_listings.LOCATION)
        industry = request.args.get(job_listings.INDUSTRY)
        seniority = request.args.get(job_listings.SENIORITY)

        job_listings_list = job_listings.search_job_with_filters(title, company, location, industry, seniority)

        if job_listings_list:
            [job.pop("applicants", None) for job in job_listings_list]  # Remove applicants data
            [job.pop("selected", None) for job in job_listings_list]
            return job_listings_list, HTTPStatus.OK
        else:
            return {"error":"Not found any"}, HTTPStatus.NOT_FOUND
        
    @api.doc("Post a new job listing")
    @api.expect(JOB_LISTING_CREATE_FLDS)
    @api.doc(security='apikey')
    @jwt_required()
    def post(self):
        if "name" not in current_user:
            return "Only companies can create a job posting", 401
        
        company = current_user["name"]
        title = request.json.get(job_listings.TITLE)
        location = request.json.get(job_listings.LOCATION)
        industry = request.json.get(job_listings.INDUSTRY)
        seniority = request.json.get(job_listings.SENIORITY)
        
        new_job_id = job_listings.create_job_listing(title, company, location, industry, seniority)
        print(f"Created job post with id: {new_job_id}")
        return {"message": "Job listing created", "job_id": str(new_job_id)}, HTTPStatus.OK
    
    @api.doc("Update a specific job listing")
    @api.expect(JOB_LISTING_UPDATE_FLDS)
    @api.doc(security='apikey')
    @jwt_required()
    def put(self):
        if "name" not in current_user:
            return "Only companies can update a job posting", 401
        
        company = current_user["name"]
        job_id = request.json.get("id")
        title = request.json.get(job_listings.TITLE)
        location = request.json.get(job_listings.LOCATION)
        industry = request.json.get(job_listings.INDUSTRY)
        seniority = request.json.get(job_listings.SENIORITY)

        print("job_id", job_id)
        
        update_job = job_listings.update_job_listing(job_id, title, company, location, industry, seniority)
        if update_job == "Not allowed":
            return "You are not allowed to modify other company's job board", 401
        elif update_job:
            return "Job listing updated", HTTPStatus.OK
        else:
            return "Cannot find the job you looking for", HTTPStatus.NOT_FOUND

@api.route("/<id>")
@api.response(HTTPStatus.OK, "Success")
@api.response(HTTPStatus.NOT_FOUND, "Job Listing Not Found")
class JobListingResource(Resource):
    @api.doc("Get job listing details")
    @api.doc(security='apikey')
    @jwt_required()
    def get(self, id):
        job = job_listings.get_job_listing_by_id(id)
        if job:
            return job, HTTPStatus.OK
        else:
            return "Job not found", HTTPStatus.NOT_FOUND

    @api.doc("Delete a specific job listing")
    @api.doc(security='apikey')
    @jwt_required()        
    def delete(self, id):
        if "name" not in current_user:
            return "Only companies can delete a job posting", 401
        company = current_user["name"]
        delete_job = job_listings.delete_job_listing(id, company)
        if delete_job == "Not allowed":
            return "You are not allowed to modify other company's job board", 401 
        elif delete_job:
            return "Job listing deleted", HTTPStatus.OK
        else:
            return "Cannot find the job you looking for", HTTPStatus.NOT_FOUND

@api.route("/<id>/applicants")
@api.response(HTTPStatus.OK, "Success")
@api.response(HTTPStatus.NOT_FOUND, "Job Listing Not Found")
class JobListingApplicants(Resource):
    @api.doc("View all applicants for the current job posting")
    @api.doc(security='apikey')
    @jwt_required()
    def get(self, id):
        if "name" not in current_user:
            return "Only companies can view applicants", 401
        company = current_user["name"]
        applicants = job_listings.view_applicants(id, company)
        if applicants == "Not allowed":
            return "You are not allowed to view applicants from other company's job posting", 401 
        elif applicants is not None:
            return applicants, HTTPStatus.OK
        else:
            return "Cannot find the job you looking for", HTTPStatus.NOT_FOUND
        
@api.route("/show_details") #show all details of all job listings of the current company
@api.response(HTTPStatus.OK, "Success")
@api.response(HTTPStatus.NOT_FOUND, "Job Listing Not Found")
class CompanyShowListings(Resource):
    @api.doc("Show all details of all job listings of the current company")
    @api.doc(security='apikey')
    @jwt_required()
    def get(self):
        if "name" not in current_user:
            return "Only companies can view their job postings", 401
        company = current_user["name"]
        print("company", company)
        job_listings_list = job_listings.search_job_with_filters(None, company, None, None, None)
        applicants = []
        for job in job_listings_list:
            for applicant in job["applicants"]:
                applicants.append({applicant:(job["_id"], job["title"])})

        if job_listings_list:
            return [job_listings_list,applicants], HTTPStatus.OK
        else:
            return [[], []], HTTPStatus.OK

@api.route("/apply/<id>")  # for job seekers
@api.response(HTTPStatus.OK, "Success")
@api.response(HTTPStatus.NOT_FOUND, "Job Listing Not Found")
class JobSeekerManagement(Resource):
    @api.doc("Apply to a specific job listing")
    @api.doc(security='apikey')
    @jwt_required()        
    def put(self, id):
        if "first" not in current_user:
            return {"error":"Only signed-in job seekers can apply for job postings"}, 401
        email = current_user['email']
        candidate = job_listings.update_applicant(id, email)
        if candidate == "applied":
            return {"error":"You had applied for this position already!"}, 400
        elif candidate:

            # Log the AB testing event
            session_id = get_session_id()
            request_data = request.get_json(silent=True)
            
            if request_data and "ABTestingVarient" in request_data:
                varient = request_data["ABTestingVarient"]

            abtest.log_ab_test_event(session_id, varient, f"applied to {job_listings.get_job_listing_by_id(id)['title']}")
            return {"message":"Applied succesfully!"}, HTTPStatus.OK
        else:
            return {"error":"Cannot find the job you looking for"}, HTTPStatus.NOT_FOUND


@api.route("/select/<action>") # for companies
@api.response(HTTPStatus.OK, "Success")
@api.response(HTTPStatus.NOT_FOUND, "Job Listing Not Found")
class JobSeekerSelection(Resource):
    @api.doc("Select an applicant for a specific job listing")
    @api.expect(JOB_LISTING_SELECT_FLDS)
    @api.doc(security='apikey')
    @jwt_required()        
    def put(self, action):
        if "name" not in current_user:
            return "Only companies can select applicants", 401
        company = current_user["name"]
        job_id = request.json.get("id") #job id
        email = request.json.get("email") #applicant email

        if not validate_email(email):
            return {"error": "Not appropriate email format"}, 400
        
        if action != "accept" and action != "reject": 
            return {"error": "Not appropriate action"}, 400
            
        candidate = job_listings.select_applicant(job_id, company, email, action)

        if candidate == "Not applied":
            return "The applicant cannot be found on this job posting's applicant list!", HTTPStatus.NOT_FOUND
        elif candidate == "Not allowed":
            return "You are not allowed to view applicants from other company's job posting!", 401
        elif candidate == "selected":
            return "The applicant had already been selected for this job posting!", HTTPStatus.NOT_FOUND
        elif candidate:
            return "Selected succesfully!", HTTPStatus.OK
        else:
            return "Cannot find the job you looking for.", HTTPStatus.NOT_FOUND
        
@api.route("/job_seeker/applications")
@api.response(HTTPStatus.OK, "Success")
@api.response(HTTPStatus.NOT_FOUND, "Job Listing Not Found")
class JobSeekerApplications(Resource):
    @api.doc("Get all job listings that a job seeker has applied to")
    @api.doc(security='apikey')
    @jwt_required()
    def get(self):
        if "first" not in current_user:
            return "Only job seekers can view their applications", 401
        email = current_user["email"]
        applications = job_listings.get_all_jobs_for_a_job_seeker(email)
        return applications, HTTPStatus.OK