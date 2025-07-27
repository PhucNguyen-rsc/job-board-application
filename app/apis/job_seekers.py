from flask_restx import Namespace, Resource, fields
from ..db import job_seekers
from app.db import abtest
from http import HTTPStatus
from flask import jsonify, request, session
from bson.json_util import dumps
from flask_jwt_extended import create_access_token, set_access_cookies, get_jwt_identity, jwt_required, current_user
from datetime import datetime, timedelta
from .utils import validate_email, is_valid_password #validate emails and passwords
from .llm import AIService
import time
import uuid

# TODO: Check if we can use email address as username
#       Change the status codes
#       Hash the passwords
#       Implement tests


# ISSUES: There is no check if there is duplicate username

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

def get_session_id():
    if "session_id" not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']
        

api = Namespace("job_seekers", description="Endpoint for job seekers API", authorizations=authorizations)

JOB_SEEKER_CREATE_FLDS = api.model(
    "AddNewJobSeekerEntry",
    {
        job_seekers.FIRST: fields.String,
        job_seekers.LAST: fields.String,
        job_seekers.EMAIL: fields.String,
        job_seekers.EXPERTISE: fields.String,
        job_seekers.YEARS: fields.Integer,
        job_seekers.PASSWORD: fields.String
    },
)

JOB_SEEKER_UPDATE_FLDS = api.model(
    "UpdateJobSeekerEntry",
    {
        job_seekers.FIRST: fields.String,
        job_seekers.LAST: fields.String,
        job_seekers.EMAIL: fields.String,
        job_seekers.EXPERTISE: fields.String,
        job_seekers.YEARS: fields.Integer,
    },
)

JOB_SEEKER_LOGIN_FLDS = api.model(
    "LoginJobSeekerEntry",
    {
        job_seekers.EMAIL: fields.String,
        job_seekers.PASSWORD: fields.String
    }
)

SURVEY_AB_FLDS = api.model(
    "SurveyAB",
    {
        "clickedButton": fields.String,
        "experience": fields.String,
        "impactedDecision": fields.String,
        "variant": fields.String,
    }
)

@api.route("/")
@api.response(HTTPStatus.OK, "Success")
@api.response(404, "Student not found")
@api.response(400, "Wrong email format")
@api.response(HTTPStatus.CONFLICT, "Email already exists")
class JobSeekersList(Resource):
    @api.doc("List all job seekers")
    def get(self):
        job_seeker_list = job_seekers.get_job_seekers()
        if job_seeker_list:
            [seeker.pop("applied", None) for seeker in job_seeker_list] # hide credentials --> only the candidate can see this
            [seeker.pop("accepted", None) for seeker in job_seeker_list] # UNHIDE
            [seeker.pop("password", None) for seeker in job_seeker_list]
            return job_seeker_list, HTTPStatus.OK
        else:
            return "Not found", HTTPStatus.NOT_FOUND

    # Need to remove this when register is fully implemented
    @api.expect(JOB_SEEKER_CREATE_FLDS)
    def post(self):
        first_name = request.json.get(job_seekers.FIRST)
        last_name = request.json.get(job_seekers.LAST)
        email = request.json.get(job_seekers.EMAIL)
        expertise = request.json.get(job_seekers.EXPERTISE)
        years = request.json.get(job_seekers.YEARS)
        password = request.json.get(job_seekers.PASSWORD)

        # Validate email
        if not validate_email(email):
            print(f"Invalid email format: {email}")
            return {"error": "Invalid email format"}, 400

        # Check if email already exists
        record = job_seekers.find_job_seeker(email)
        print(f"Checking for existing email: {email} - Found: {record}")  # Debug print

        if record:
            print(f"Duplicate email found: {email}")
            return {"error": "The email address already exists"}, HTTPStatus.CONFLICT
        else:
            job_seeker_id = job_seekers.create_job_seeker(first_name, last_name, email, expertise, years, password)
            print(f"Created job seeker with id: {job_seeker_id}")
            return {"message": "Job seeker created", "id": str(job_seeker_id)}, HTTPStatus.OK

    
@api.route("/<email>")
@api.param("email", "Job Seeker email to use for lookup")
@api.response(HTTPStatus.OK, "Success")
@api.response(HTTPStatus.NOT_ACCEPTABLE, "Not acceptable")
@api.response(404, "Job Seeker not found")
@api.response(400, "Wrong email format")
class JobSeekers(Resource):

    @api.doc("Filter job seeker by their email")
    def get(self, email):
        # Validate email
        if not validate_email(email):
            return {"error": "Invalid email format"}, 400
        
        job_seeker = job_seekers.find_job_seeker(email)
        if job_seeker:
            return job_seeker, HTTPStatus.OK
        else:
            return "Not found", HTTPStatus.NOT_FOUND
        
    @api.expect(JOB_SEEKER_UPDATE_FLDS)
    @api.doc("Update a specific job seeker, identified by email")
    def put(self, email):
        first_name = request.json.get(job_seekers.FIRST)
        last_name = request.json.get(job_seekers.LAST)
        new_email = request.json.get(job_seekers.EMAIL)
        expertise = request.json.get(job_seekers.EXPERTISE)
        years = request.json.get(job_seekers.YEARS)

        # Validate email
        if not validate_email(email) or not validate_email(new_email):
            return "Not approriate email format", 400

        updated_job_seeker = job_seekers.update_job_seeker(email, first_name, last_name, new_email, expertise, years)

        if updated_job_seeker is None:
            return "Job seeker email not found", HTTPStatus.NOT_FOUND

        return "Job seeker updated", HTTPStatus.OK

    @api.doc("Delete a specific job seeker, identified by email")    
    def delete(self, email):
        # Validate email
        if not validate_email(email):
            return "Not approriate email format", 400
        
        delete_job_seeker = job_seekers.delete_job_seeker(email)

        if delete_job_seeker is None:
            return "Job seeker email not found", HTTPStatus.NOT_FOUND

        return "Job seeker deleted", HTTPStatus.OK
    
    
@api.route("/login")
@api.response(HTTPStatus.OK, "Success")
@api.response(404, "Job Seeker not found")
@api.response(400, "Wrong email format")
@api.expect(JOB_SEEKER_LOGIN_FLDS)
@api.doc("Log In users")
class JobSeekers(Resource):
    def post(self):
        email = request.json.get(job_seekers.EMAIL)
        password = request.json.get(job_seekers.PASSWORD)

        # Validate email
        if not validate_email(email): #check if "" and None also
            return {"error":"Not approriate email format"}, 400
        
        userEntry = job_seekers.find_job_seeker(email)
        
        # TODO: Refine the login checking logic
        if (userEntry and job_seekers.check_login_credentials(email, password)):
            access_token = create_access_token(
                identity=userEntry, expires_delta=timedelta(hours=0.5)
            )
            
            response = jsonify({
                "message": "Logged in Successfully",
                "access_token": access_token
            })
            
            return response
        
        return {"error":"Bad credentials"}, 401
    
    
@api.route("/signup")
@api.response(HTTPStatus.OK, "Success")
@api.response(HTTPStatus.CONFLICT, "Email already exists")
@api.response(400, "Wrong email format")
@api.expect(JOB_SEEKER_CREATE_FLDS)
@api.doc("Sign up users")
class JobSeekers(Resource):
    def post(self):
        first_name = request.json.get(job_seekers.FIRST)
        last_name = request.json.get(job_seekers.LAST)
        email = request.json.get(job_seekers.EMAIL)
        expertise = request.json.get(job_seekers.EXPERTISE)
        years = request.json.get(job_seekers.YEARS)
        password = request.json.get(job_seekers.PASSWORD)

        # Validate email
        if not validate_email(email):
            return {"error": "Not approriate email format"}, 400
        
        # Validate password strength
        if not is_valid_password(password):
            return {"error": "Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, and a number"}, 400
        
        record = job_seekers.find_job_seeker(email)

        if record:
            return {"error":"The email address already exists"}, HTTPStatus.CONFLICT
        else:
            job_seeker_id = job_seekers.create_job_seeker(first_name, last_name, email, expertise, years, password)
            print(f"Created job seeker with id: {job_seeker_id}")
            return {"message": "Job seeker Registered Successfully"}, HTTPStatus.OK
        
        
@api.route("/find")
@api.response(HTTPStatus.OK, "Success")
@api.response(HTTPStatus.CONFLICT, "Email already exists")
class JobSeekers(Resource):
    @api.doc("testing functionality of jwt")
    @api.doc(security='apikey')
    @jwt_required()
    def get(self):
        return {"message":f"Hello {current_user['first']}"}, HTTPStatus.OK
    

@api.route("/inquire")
@api.response(HTTPStatus.OK, "Success")
class JobSeekers(Resource):
    @api.doc("Inquire job status of the current registered job seeker")
    @api.doc(security='apikey')
    @jwt_required()
    def get(self):
        if not "first" in current_user: #job seekers
            return {"error":"Only signed-in job seekers can see their own application status"}, 401
        
        email = current_user['email']
        apply_data = job_seekers.inquire_status(email)

        return {"data":apply_data}, HTTPStatus.OK


ai_service = AIService()
AI_SUGGESTION_RESPONSE = api.model(
    "AISuggestionResponse",
    {
        "matchAnalysis": fields.String,
        "tips": fields.List(fields.String),
        "score": fields.Float,
        "strengths": fields.List(fields.String)
    }
)

AI_SUGGESTION_FLDS = api.model(
    "AISuggestionRequest",
    {
        "job": fields.Nested(api.model("JobDetails", {
            "title": fields.String,
            "company": fields.String,
            "location": fields.String,
            "industry": fields.String,
            "seniority": fields.Integer,
            # Add other job fields as needed
        })),
        "applicant": fields.Nested(api.model("ApplicantDetails", {
            "first": fields.String,
            "last": fields.String,
            "email": fields.String,
            "expertise": fields.String,
            "years": fields.Integer,
            # Add other applicant fields as needed
        }))
    }
)
@api.route("/ai/suggestions")
@api.response(HTTPStatus.OK, "Success")
@api.response(400, "Invalid request")
@api.response(401, "Unauthorized")
@api.response(429, "Too many requests")
@api.response(500, "AI service error")
class AISuggestions(Resource):
    @api.expect(AI_SUGGESTION_FLDS)
    @api.marshal_with(AI_SUGGESTION_RESPONSE)
    @api.doc(security='apikey')
    @jwt_required()
    def post(self):
        print(1)
        """
        Get AI-powered suggestions for a job application
        ---
        Returns AI-generated suggestions for improving job application match
        including match score, analysis, tips, and strengths to highlight.
        """
        try:
            # Get and validate input data
            data = request.get_json(force=True)
            if not data:
                api.abort(400, "Request body must be JSON")
            
            job = data.get("job")
            applicant = data.get("applicant")
            
            if (not job or not applicant):
                api.abort(400, "Both job and applicant data are required")

            # Validate required fields
            required_job_fields = {
                'title': str,
                'company': str,
                'location': str,
                'industry': str,
                'seniority': int
            }
            
            required_applicant_fields = {
                'first': str,
                'last': str,
                'email': str,
                'expertise': str,
                'years': int
            }

            # Validate job fields
            print("job: ",job)
            print("applicant: ",applicant)
            for field, field_type in required_job_fields.items():
                if field not in job:
                    api.abort(400, f"Missing required job field: {field}")

            # Validate applicant fields
            for field, field_type in required_applicant_fields.items():
                if field not in applicant:
                    api.abort(400, f"Missing required applicant field: {field}")

            session_id = get_session_id()

             # Try to get the variant from cookies first
            varient = request.cookies.get("AB_testing_varient")
            # If not in cookies, try to get it from the request body as fallback
            if not varient and data.get("ABTestingVarient"):
                varient = data.get("ABTestingVarient")

            abtest.log_ab_test_event(session_id, varient,  f"view AI suggestions for {job['title']}")

            # Rate limiting (1 request per 30 seconds)
            time.sleep(31)
            # Get AI suggestions
            suggestions = ai_service.generate_suggestions(job, applicant)
            if not suggestions:
                api.abort(500, "AI service returned empty response")
        
           

            # Format response
            return {
                "matchAnalysis": suggestions.get("analysis", "No analysis available"),
                "tips": suggestions.get("suggestions", []),
                "score": float(suggestions.get("matchScore", 0)),
                "strengths": suggestions.get("strengths", [])
            }, HTTPStatus.OK

        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, "Internal server error while generating AI suggestions")


@api.route("/ab_survey")
@api.response(HTTPStatus.OK, "Success")
@api.response(400, "Invalid request")
class SurveySubmission(Resource):
    @api.expect(SURVEY_AB_FLDS)
    @jwt_required()
    def post(self):
        """
        Collect and parse data for AB Testing
        """
        # Get and validate input data
        print("JSON Request:", request.json)
        clickedButton = request.json.get("clickedButton")
        experience = request.json.get("experience")
        impactedDecision = request.json.get("impactedDecision")
        variant = request.json.get("variant")
        session_id = get_session_id()

        print("experience", experience)

        abtest.log_ab_test_survey(session_id, clickedButton, experience, impactedDecision, variant)

        return {"message": "Submit succesfully"}, HTTPStatus.OK 
 
