from app.db.constants import COMPANY_COLLECTION, NAME, COMPANY_EMAIL, COUNTRY, DESCRIPTION, PASSWORD
from app.db.utils import serialize_item, serialize_items
import app.db.job_listings as job_listings
from .db import get_db

# HASHING PASSWORDS
import bcrypt  


def _get_company_collection():
    db = get_db()
    return db[COMPANY_COLLECTION]

def get_companies():
    companies = _get_company_collection().find({})
    return serialize_items(list(companies))

def find_company(email: str = None):
    query = {}
    if email is not None:
        query[COMPANY_EMAIL] = {'$regex': email}

    company = _get_company_collection().find_one(query)
    return serialize_item(company) 

def find_company_by_name(name: str):
    query = {NAME: {'$regex': f'^{name}$', '$options': 'i'}}  # Case-insensitive match
    company = _get_company_collection().find_one(query)
    return serialize_item(company)


def create_company(name: str, email: str, country: str, description: str, password: str):
    #Convert name to lowercase to enforce uniqueness
    name = name.strip().lower()

    #Deliverable 4 - Hash the password here, where 'password' is defined
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    new_company = {
        NAME: name,
        COMPANY_EMAIL: email,
        COUNTRY: country,
        DESCRIPTION: description,
        PASSWORD: hashed_password.decode('utf-8')  # store as string
    }
    
    result = _get_company_collection().insert_one(new_company)
    return result.inserted_id

def update_company(lookupemail: str, name: str, email: str, country: str, description: str):
    company_record = find_company(lookupemail)

    if company_record is None:
        return None

    new_company = {NAME: name, COMPANY_EMAIL: email, COUNTRY: country, DESCRIPTION: description}
    result = _get_company_collection().update_one({COMPANY_EMAIL: lookupemail}, {"$set": new_company})

    return result

def delete_company(email: str):
    company_record = find_company(email)

    if company_record is None:
        return None
    
    # Delete all job listings for the company
    job_listing_posted = job_listings.search_job_with_filters(company=company_record[NAME])
    for job_listing in job_listing_posted:
        job_listings.delete_job_listing(job_listing["_id"], company_record[NAME])

    result = _get_company_collection().delete_one({COMPANY_EMAIL: email})
    return result

def check_login_credentials(email: str, password: str):
    if email is None or password is None:
        return None

    company = _get_company_collection().find_one({COMPANY_EMAIL: email})
    if not company:
        return None

    stored_hashed_pw = company.get(PASSWORD)
    if stored_hashed_pw and bcrypt.checkpw(password.encode('utf-8'), stored_hashed_pw.encode('utf-8')):
        return company  # password matches

    return None  # invalid password
