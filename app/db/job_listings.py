from app.db.constants import JOB_LISTING_COLLECTION, TITLE, COMPANY, LOCATION, INDUSTRY, SENIORITY, APPLICANTS, SELECTED, REJECTED
from app.db.utils import serialize_item, serialize_items, generate_slug
from .db import get_db
import re
from bson.objectid import ObjectId
import app.db.job_seekers as job_seekers


def _get_job_listing_collection():
    db = get_db()
    return db[JOB_LISTING_COLLECTION]

# to make sure the job search works, we have to make the entries into slug-like
def search_job_with_filters(title: str = None, company: str = None, location: str= None, industry: str = None, seniority: str = None): #search for either email or name # update to filter    
    query = {}
    if company:
        query[COMPANY] = {'$regex': generate_slug(company)} #so that it can match regardless
    if title :
        query[TITLE] = {'$regex': generate_slug(title)}
    if location:
        query[LOCATION] = {'$regex': generate_slug(location)}
    if industry:
        query[INDUSTRY] = {'$regex': generate_slug(industry)}
    if seniority:
        query[SENIORITY] = {'$regex': generate_slug(seniority)} #seniority have to be string instead of interger

    listing = _get_job_listing_collection().find(query) #how to make sure there only one?
    return serialize_items(listing)


def search_job_with_id(id: str): #intend to be used internally
    record = _get_job_listing_collection().find_one({"_id": ObjectId(id)}) #store id version
    return record

def get_job_listing_by_id(job_id: str):
    record = search_job_with_id(job_id)
    if record:
        return serialize_item(record)
    return None


def create_job_listing(title: str, company: str, location: str, industry: str, seniority: str):
    new_job_listing = {
        TITLE: generate_slug(title),
        COMPANY: generate_slug(company), #company name
        LOCATION: generate_slug(location),
        INDUSTRY: generate_slug(industry),
        SENIORITY: generate_slug(seniority),
        APPLICANTS: [] , # applicants list
        SELECTED: [], # selected list
        REJECTED: []
    }

    result = _get_job_listing_collection().insert_one(new_job_listing)
    return result.inserted_id #use this id in frontend


def update_job_listing(id: str, title: str, company: str, location: str, industry: str, seniority: str): # one specific job listing
    job_list_record = search_job_with_id(id) # assume this will give out a specific role only

    if job_list_record is None:
        return None
    
    if job_list_record[COMPANY] != generate_slug(company): #only that company can modify its own job board
        return "Not allowed"

    new_job_listing = {
        TITLE: generate_slug(title),
        COMPANY: generate_slug(company), #company name
        LOCATION: generate_slug(location),
        INDUSTRY: generate_slug(industry),
        SENIORITY: generate_slug(seniority),
        APPLICANTS: job_list_record[APPLICANTS], # empty applicants list
        SELECTED: job_list_record[SELECTED], # selected list,
        REJECTED: job_list_record[REJECTED],
    }

    print("update_job_listing", new_job_listing)

    result = _get_job_listing_collection().update_one(
        {"_id": ObjectId(id)},  
        {"$set": new_job_listing}
    )

    return result


def delete_job_listing(id: str, company: str): # one specific job listing
    job_list_record = search_job_with_id(id) 

    if job_list_record is None:
        return None
    
    if job_list_record[COMPANY] != generate_slug(company): # only that company can modify its own job board
        return "Not allowed"
    
    # Delete job listing from the job seeker's applied / selected / rejected list
    for applicant in job_list_record[APPLICANTS]:
        job_seekers.remove_job_listing_from_job_seeker(id, applicant)

    for applicant in job_list_record[SELECTED]:
        job_seekers.remove_job_listing_from_job_seeker(id, applicant)

    for applicant in job_list_record[REJECTED]:
        job_seekers.remove_job_listing_from_job_seeker(id, applicant)
    
    result = _get_job_listing_collection().delete_one({"_id": ObjectId(id)})
    return result

def view_applicants(id: str, company: str):
    job_list_record = search_job_with_id(id) 

    if job_list_record is None:
        return None
    
    if job_list_record[COMPANY] != generate_slug(company): # only that company can modify its own job board
        return "Not allowed"

    return job_list_record[APPLICANTS]


def update_applicant(id: str, email: str):
    job_list_record = search_job_with_id(id)

    if job_list_record is None:
        return None
    
    if email in job_list_record[APPLICANTS] or email in job_list_record[SELECTED] or email in job_list_record[REJECTED]: #already applied
        return "applied"
    
    applicant = job_seekers.apply(id, email)
    result = _get_job_listing_collection().update_one(
        {"_id": ObjectId(id)},  # Find the document by _id
        {"$push": {APPLICANTS: email}}  # Append to list
    )

    return result

def select_applicant(id: str, company: str, email: str, action: str): #either accept or reject
    job_list_record = search_job_with_id(id)

    if job_list_record is None:
        return None
    
    if job_list_record[COMPANY] != generate_slug(company): # only that company can modify its own job board
        return "Not allowed"
    
    if email not in job_list_record[APPLICANTS]: 
        return "Not applied" # not found applicants on the list
    
    if email in job_list_record[SELECTED]:
        return "selected"

    applicant = job_seekers.changeStatus(id, email, action)

    result = _get_job_listing_collection().update_one(
        {"_id": ObjectId(id)}, 
        {"$pull": {APPLICANTS: email}}  # Remove from list
    )

    if action == "accept":
        result = _get_job_listing_collection().update_one(
            {"_id": ObjectId(id)},  # Find the document by _id
            {"$push": {SELECTED: email}}  # Append to list
        )
    elif action == "reject":
        result = _get_job_listing_collection().update_one(
            {"_id": ObjectId(id)},  # Find the document by _id
            {"$push": {REJECTED: email}}  # Append to list
        )

    return result

# Get all job listings that a job seeker has applied to
def get_all_jobs_for_a_job_seeker(jobSeekerEmail: str):
    query = {}
    query[APPLICANTS] = jobSeekerEmail

    listing = _get_job_listing_collection().find(query)
    return serialize_items(listing)

# Remove job seeker from the job listing
def remove_job_seeker_from_job_listing(jobListingId: str, jobSeekerEmail: str):

    print(jobListingId, jobSeekerEmail)

    result = _get_job_listing_collection().update_one(
        {"_id": ObjectId(jobListingId)},
        {
            "$pull": {
                APPLICANTS: jobSeekerEmail,
                SELECTED: jobSeekerEmail,
                REJECTED: jobSeekerEmail
            }
        }
    )
    return result
