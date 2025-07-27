from app.db.constants import JOB_SEEKER_COLLECTION, FIRST, LAST, EMAIL, EXPERTISE, YEARS, PASSWORD, APPLIED, ACCEPTED, REJECTED
from app.db.utils import serialize_item, serialize_items
from .db import get_db
import app.db.job_listings as job_listings

# HASHING PASSWORDS
import bcrypt  

def _get_job_seekers_collection():
    db = get_db()
    return db[JOB_SEEKER_COLLECTION]

# Returns the entire list of job seekers
def get_job_seekers():
    job_seekers = _get_job_seekers_collection().find()
    return serialize_items(list(job_seekers))

# Finds ONE job seeker that has the matching email
def find_job_seeker(email: str = None):
    query = {}
    if email is not None:
        query[EMAIL] = {'$regex': email}

    job_seeker = _get_job_seekers_collection().find_one(query)
    return serialize_item(job_seeker)

def create_job_seeker(first_name: str,
                      last_name: str,
                      email: str,
                      expertise: str,
                      years: int,
                      password: str):

    #Deliverable 4 - hash before storing
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    job_seeker = {
        FIRST: first_name,
        LAST: last_name,
        EMAIL: email,
        EXPERTISE: expertise,
        YEARS: years,
        PASSWORD: hashed_pw.decode('utf-8'),   # store as string
        APPLIED: [],
        ACCEPTED: [],
        REJECTED: []
    }

    result = _get_job_seekers_collection().insert_one(job_seeker)
    return result.inserted_id


def update_job_seeker(lookupemail: str, first_name: str, last_name: str, email: str, expertise: str, years: int):
    job_seeker_record = find_job_seeker(lookupemail)

    if job_seeker_record is None:
        return None

    new_data = {
        FIRST: first_name, 
        LAST: last_name, 
        EMAIL: email, 
        EXPERTISE: expertise, 
        YEARS: years
    }
    
    # Preserve the existing applied, accepted, and rejected fields if they exist
    if APPLIED in job_seeker_record:
        new_data[APPLIED] = job_seeker_record[APPLIED]
    if ACCEPTED in job_seeker_record:
        new_data[ACCEPTED] = job_seeker_record[ACCEPTED]
    if REJECTED in job_seeker_record:
        new_data[REJECTED] = job_seeker_record[REJECTED]
        
    result = _get_job_seekers_collection().update_one({EMAIL: lookupemail}, {"$set": new_data})

    return result


def delete_job_seeker(lookupemail: str):
    record = find_job_seeker(lookupemail)

    print(record)

    if record is None:
        return None

    # Delete job seeker from all job listings that the job seeker has applied to
    for job_listing_id in record[APPLIED]:
        job_listings.remove_job_seeker_from_job_listing(job_listing_id, lookupemail)

    for job_listing_id in record[ACCEPTED]:
        job_listings.remove_job_seeker_from_job_listing(job_listing_id, lookupemail)

    for job_listing_id in record[REJECTED]:
        job_listings.remove_job_seeker_from_job_listing(job_listing_id, lookupemail)

    result = _get_job_seekers_collection().delete_one({EMAIL: lookupemail})
    return result


def check_login_credentials(email: str, password: str):
    # Return the job‑seeker document if the (email, password) pair is valid,
    # otherwise return None.
    
    # look up the user by email only
    seeker = _get_job_seekers_collection().find_one({EMAIL: email})
    if not seeker:
        return None                    # email not found

    stored_hash = seeker.get(PASSWORD)  # hash saved in DB
    if stored_hash and bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return seeker                  # password matches

    return None                        # bad password


def apply(id, email): #applicants apply for a job
    record = find_job_seeker(email)

    # if record is None: # never gonna happen if we only use it internaly (not as endpoints)
    #     return "not found"
    
    result = _get_job_seekers_collection().update_one(
        {"email": email},  # Find the document by _id
        {"$push": {APPLIED: id}}  # Append to list
    )

    return result

def changeStatus(id: str, email: str, action: str): #appicants get accepted for a job
    record = find_job_seeker(email)
    
    result = _get_job_seekers_collection().update_one(
        {"email": email},  # Find the document by _id
        {"$pull": {APPLIED: id}}  # remove from list
    )

    if action == "accept":
        result = _get_job_seekers_collection().update_one(
            {"email": email},  # Find the document by _id
            {"$push": {ACCEPTED: id}}  # Append to list
        )
    elif action == "reject":
        result = _get_job_seekers_collection().update_one(
            {"email": email},  # Find the document by _id
            {"$push": {REJECTED: id}}  # Append to list
        )

    return result

    
def translate_slug(slug: str):
    normal_text = slug.replace("-", " ")
    normal_text = normal_text.title()
    return normal_text

def findJobDetails(id):
    job = job_listings.search_job_with_id(id)
    return (job["title"], job["company"], job["location"], job["industry"], job["seniority"])


def inquire_status(email):
    record = find_job_seeker(email)
    apply_data = {}

    for entry in record[ACCEPTED]:
        information = findJobDetails(entry)
        apply_data[entry] = ("accepted", information)

    for entry in record[REJECTED]:
        information = findJobDetails(entry)
        apply_data[entry] =  ("rejected", information)

    for entry in record[APPLIED]:
        if entry not in record[ACCEPTED] and entry not in record[REJECTED]:
            information = findJobDetails(entry)
            apply_data[entry] = ("waiting", information)   
    
    return apply_data

def remove_job_listing_from_job_seeker(jobListingId: str, jobSeekerEmail: str):
    result = _get_job_seekers_collection().update_one(
        {"email": jobSeekerEmail},
        {"$pull": {
                APPLIED: jobListingId,
                ACCEPTED: jobListingId,
                REJECTED: jobListingId
            }
        }
    )
    return result

