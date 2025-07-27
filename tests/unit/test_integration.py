from .utils import normalize_text, assert_items_equal
from bson.objectid import ObjectId
from app.db.constants import JOB_LISTING_COLLECTION, JOB_SEEKER_COLLECTION, COMPANY_COLLECTION

# CRUD tests for companies operations
def test_company_CRUD(client):
    """
    Integration test to verify the full company CRUD.
    """

    # 1. Create a new company
    new_company = {
        "name": "Test",
        "email": "test@company.com",
        "country": "UAE",
        "description": "Test company"
    }
    response = client.post("/api/companies/", json=new_company)
    assert response.status_code == 200 # nosec B101

    # Expecting a JSON dict with {"message": "..."}
    resp_json = response.get_json()
    assert isinstance(resp_json, dict) # nosec B101
    assert resp_json["message"] == "Company created" # nosec B101

    # 2. GET the company and verify data
    response = client.get("/api/companies/test@company.com")
    assert response.status_code == 200 # nosec B101
    assert_items_equal(response.json, new_company)
    
    # 3. UPDATE the company
    updated_company = {
        "name": "Updated Test Company",
        "email": "test@company.com",
        "country": "US",
        "description": "Updated description"
    }

    response = client.put("/api/companies/test@company.com", json=updated_company)    
    assert response.status_code == 200 # nosec B101    
    assert response.json == "Company updated" # nosec B101

    # 4. GET again and verify update
    response = client.get("/api/companies/test@company.com")
    assert response.status_code == 200 # nosec B101    
    assert_items_equal(response.json, updated_company)

    # 5. DELETE the company
    response = client.delete("/api/companies/test@company.com")
    assert response.status_code == 200 # nosec B101    
    assert response.json == "Company deleted" # nosec B101

    # 6. VERIFY deletion
    response = client.get("/api/companies/test@company.com")    
    assert response.status_code == 404 # nosec B101


def test_companies_CRUD_failed(client):
    """
    Integration test to verify the failling fallbacks of company CRUD.
    """

    # 1. Create a new company
    new_company = {
        "name": "Test",
        "email": "test@company.com",
        "country": "UAE",
        "description": "Test company"
    }
    response = client.post("/api/companies/", json=new_company)
    assert response.status_code == 200 # nosec B101

    # 2. Create the same company with same address
    new_company = {
        "name": "Test",
        "email": "test@company.com",
        "country": "UAE",
        "description": "Test company"
    }

    response = client.post("/api/companies/", json=new_company)
    assert response.status_code == 409 # nosec B101
    assert response.json == {"error": "The email address already exists"} # nosec B101


    fake_email = "nonexisten_email@nyu.edu"
    response = client.delete(f"/api/companies/{fake_email}")
    assert response.status_code == 404 # nosec B101
    assert response.json == "Company email not found" # nosec B101

    bad_signup_email = {
        "email": "test@company.com", #already exists email
        "password": "Testname123", 
        "name": "Nonexistent",
        "country": "China",
        "description": "fake company"
    }
    response = client.post("/api/companies/signup", json=bad_signup_email)
    assert response.status_code == 409 # nosec B101
    assert response.json == {"error": "The email address already exists"} # nosec B101


    bad_signup_name = {
        "email": "test12345@company.com", 
        "password": "Testname123", 
        "name": "Test", #already exists name
        "country": "China",
        "description": "fake company"
    }
    response = client.post("/api/companies/signup", json=bad_signup_name)
    assert response.status_code == 409 # nosec B101
    assert response.json == {"error": "The company name already exists"} # nosec B101

    bad_login_email = {
        "email": "nonexistent_email@nyu.edu",
        "password": "Testname123"
    }

    response = client.post("/api/companies/login", json=bad_login_email)
    assert response.status_code == 401 # nosec B101
    assert response.json == {'error': 'Bad credentials'} # nosec B101

    # pass
    

# CRUD tests for job_seekers operations
def test_job_seeker_CRUD(client):
    """
    Integration test to verify the full job seeker CRUD.
    """

    # 1. Create a new job seeker
    new_job_seeker = {
        "first": "John",
        "last": "Doe",
        "email": "johndoe@test.com",
        "expertise": "Software Engineering",
        "years": 3,
        "password": "SecurePass123"
    }
    response = client.post("/api/job_seekers/", json=new_job_seeker)
    assert response.status_code == 200 # nosec B101
    
    # Expecting a JSON dict with {"message": "..."}
    resp_json = response.get_json()
    assert isinstance(resp_json, dict) # nosec B101
    assert resp_json["message"] == "Job seeker created" # nosec B101

    # 2. GET the job seeker and verify data
    response = client.get("/api/job_seekers/johndoe@test.com")
    assert response.status_code == 200 # nosec B101
    assert response.json["first"] == new_job_seeker["first"] # nosec B101
    assert response.json["last"] == new_job_seeker["last"] # nosec B101
    assert response.json["email"] == new_job_seeker["email"] # nosec B101
    assert response.json["expertise"] == new_job_seeker["expertise"] # nosec B101
    assert response.json["years"] == new_job_seeker["years"] # nosec B101
    
    # 3. UPDATE the job seeker
    updated_job_seeker = {
        "first": "John",
        "last": "Smith",
        "email": "johndoe@test.com",
        "expertise": "Data Science",
        "years": 5
    }

    response = client.put("/api/job_seekers/johndoe@test.com", json=updated_job_seeker)
    assert response.status_code == 200 # nosec B101    
    assert response.json == "Job seeker updated" # nosec B101

    # 4. GET again and verify update
    response = client.get("/api/job_seekers/johndoe@test.com")
    assert response.status_code == 200 # nosec B101    
    assert response.json["last"] == updated_job_seeker["last"] # nosec B101
    assert response.json["expertise"] == updated_job_seeker["expertise"] # nosec B101
    assert response.json["years"] == updated_job_seeker["years"] # nosec B101

    # 5. DELETE the job seeker
    response = client.delete("/api/job_seekers/johndoe@test.com")
    assert response.status_code == 200 # nosec B101    
    assert response.json == "Job seeker deleted" # nosec B101

    # 6. VERIFY deletion
    response = client.get("/api/job_seekers/johndoe@test.com")    
    assert response.status_code == 404 # nosec B101


def test_job_listings_CRUD(client):
    """
    Integration test to verify the full job listings CRUD operations.
    """
    # 1. Sign up a company
    company_data = {
        "name": "Test Company",
        "email": "company@test.com",
        "country": "US",
        "description": "ABC",
        "password": "Abcdefgh0"
    }
    response = client.post("/api/companies/signup", json=company_data)
    assert response.status_code == 200 # nosec B101
    assert response.json["message"] == "Company Registered Successfully" # nosec B101

    # 2. Sign up a job seeker
    job_seeker_data = {
        "first": "Test Job Seeker",
        "last": "Test Job Seeker",
        "email": "jobseeker@test.com",
        "expertise": "CS",
        "years": 2,
        "password": "Abcdefgh0"
    }
    response = client.post("/api/job_seekers/signup", json=job_seeker_data)
    assert response.status_code == 200 # nosec B101
    assert response.json["message"] == "Job seeker Registered Successfully" # nosec B101

    # 3. Login as company
    response = client.post("/api/companies/login", json={
        "email": "company@test.com", 
        "password": "Abcdefgh0"
    })
    assert response.status_code == 200 # nosec B101
    company_token = response.json["access_token"]

    # 4. Login as job seeker
    response = client.post("/api/job_seekers/login", json={
        "email": "jobseeker@test.com", 
        "password": "Abcdefgh0"
    })
    assert response.status_code == 200 # nosec B101
    job_seeker_token = response.json["access_token"]

    # 5. Create a new job listing using the company token
    new_job = {
        "title": "Software Engineer",
        "company": "Test Company",
        "location": "UAE",
        "industry": "Tech",
        "seniority": "Mid-Level"
    }
    response = client.post("/api/job_listings/", json=new_job, headers={
        "Authorization": f"Bearer {company_token}"
    })
    assert response.status_code == 200 # nosec B101
    resp_json = response.get_json()
    assert resp_json["message"] == "Job listing created" # nosec B101
    job_id = resp_json["job_id"]

    # 6. Retrieve all job listings and extract our job by matching _id
    response = client.get("/api/job_listings/")
    assert response.status_code == 200 # nosec B101
    listings = response.json  # this should be a list
    job_listing = next((job for job in listings if job["_id"] == job_id), None)
    assert job_listing is not None, "Job not found in job listings!" # nosec B101

    # Compare fields (assuming generate_slug converts to lowercase and hyphenates)
    expected_title = normalize_text(new_job["title"])
    expected_company = normalize_text(new_job["company"])
    expected_location = normalize_text(new_job["location"])
    expected_industry = normalize_text(new_job["industry"])
    expected_seniority = normalize_text(new_job["seniority"])

    assert job_listing["title"] == expected_title # nosec B101
    assert job_listing["company"] == expected_company # nosec B101
    assert job_listing["location"] == expected_location # nosec B101
    assert job_listing["industry"] == expected_industry # nosec B101
    assert job_listing["seniority"] == expected_seniority # nosec B101

    # 6.5 Search for job listings with filters
    response = client.get("/api/job_listings/", query_string=new_job)
    assert response.status_code == 200 # nosec B101
    listings = response.json  # this should be a list
    new_job = listings[0] # sample a random job listing

    expected_title = normalize_text(new_job["title"])
    expected_company = normalize_text(new_job["company"])
    expected_location = normalize_text(new_job["location"])
    expected_industry = normalize_text(new_job["industry"])
    expected_seniority = normalize_text(new_job["seniority"])

    assert job_listing["title"] == expected_title # nosec B101
    assert job_listing["company"] == expected_company # nosec B101
    assert job_listing["location"] == expected_location # nosec B101
    assert job_listing["industry"] == expected_industry # nosec B101
    assert job_listing["seniority"] == expected_seniority # nosec B101


    # 7. GET job listing details by ID using the company token
    response = client.get(f"/api/job_listings/{job_id}", headers={
        "Authorization": f"Bearer {company_token}"
    })
    assert response.status_code == 200 # nosec B101
    details = response.json
    assert details["_id"] == job_id # nosec B101
    assert details["title"] == expected_title # nosec B101

    # 8. Update the job listing using PUT on /job_listings/
    updated_job = {
        "id": job_id,
        "title": "Senior Software Engineer",
        "company": "Test Company",
        "location": "US",
        "industry": "Tech",
        "seniority": "Senior-Level"
    }
    response = client.put("/api/job_listings/", json=updated_job, headers={
        "Authorization": f"Bearer {company_token}"
    })
    assert response.status_code == 200 # nosec B101
    assert response.get_json() == "Job listing updated" # nosec B101

    # 9. GET updated job listing details by ID
    response = client.get(f"/api/job_listings/{job_id}", headers={
        "Authorization": f"Bearer {company_token}"
    })
    assert response.status_code == 200 # nosec B101
    updated_details = response.json
    assert updated_details["title"] == normalize_text(updated_job["title"]) # nosec B101
    assert updated_details["location"] == normalize_text(updated_job["location"]) # nosec B101
    assert updated_details["seniority"] == normalize_text(updated_job["seniority"]) # nosec B101

    # 10. Delete the job listing using DELETE on /job_listings/<id>
    response = client.delete(f"/api/job_listings/{job_id}", headers={
        "Authorization": f"Bearer {company_token}"
    })
    assert response.status_code == 200 # nosec B101
    assert response.get_json() == "Job listing deleted" # nosec B101

    # 11. Confirm deletion: GET should now return 404
    response = client.get(f"/api/job_listings/{job_id}", headers={
        "Authorization": f"Bearer {company_token}"
    })
    assert response.status_code == 404 # nosec B101


def test_job_listings_failed(client):
    """
    Integration test to verify the failing fallbacks of job listings CRUD operations.
    """
    # List all job listings wrongly
    response = client.get("/api/job_listings/", query_string={"company": "nonexistent"})
    assert response.status_code == 404 # nosec B101
    assert response.json == {'error':"Not found any"} # nosec B101

    # Unauthorized access to make new job listings
    # Scenario 1: Job seeker tries to create a new job listing
    ## Make new job listing
    new_job = {
        "title": "Software Engineer",
        "company": "Test Company",
        "location": "UAE",
        "industry": "Tech", 
        "seniority": "Mid-Level"
    }

    ## Make new job seeker
    job_seeker_data = {
        "first": "Test Job Seeker",
        "last": "Test Job Seeker",
        "email": "jobseeker@test.com",
        "expertise": "CS",
        "years": 2,
        "password": "Abcdefgh0"
    }
    response = client.post("/api/job_seekers/signup", json=job_seeker_data)

    ## Login as job seeker
    login_data = {"email": "jobseeker@test.com", "password": "Abcdefgh0"}
    response = client.post("/api/job_seekers/login", json=login_data)
    assert response.status_code == 200 # nosec B101
    job_seeker_token = response.json["access_token"]

    response = client.post("/api/job_listings/", json=new_job, headers={"Authorization": "Bearer " + job_seeker_token})
    assert response.status_code == 401 # nosec B101
    assert response.json == "Only companies can create a job posting" # nosec B101


    # Unauthorized access to update job listings
    # Scenario 1: Job seeker tries to update a job listing
    response = client.put("/api/job_listings/", json=new_job, headers={"Authorization": "Bearer " + job_seeker_token})
    assert response.status_code == 401 # nosec B101
    assert response.json == "Only companies can update a job posting" # nosec B101

    # Scenario 2: Another company tries to update your job listing
    ## Sign up another company
    first_company = {
        "name": "Test Company",
        "email": "first_company@nyu.edu",
        "country": "US",
        "description": "ABC",
        "password": "Abcdefgh0"
    }
    response = client.post("/api/companies/signup", json=first_company)
    response = client.post("/api/companies/login", json={"email": "first_company@nyu.edu", "password": "Abcdefgh0"})
    first_company_token = response.json["access_token"]

    # Register the current job for first company posting
    response = client.post("/api/job_listings/", json=new_job, headers={"Authorization": "Bearer " + first_company_token})
    current_job_id = response.json["job_id"]

    second_company = {
        "name": "Another Company",
        "email": "another@nyu.edu",
        "country": "US",
        "description": "XYZ",
        "password": "Abcdefgh0"
    }
    response = client.post("/api/companies/signup", json=second_company)
    response = client.post("/api/companies/login", json={"email": "another@nyu.edu", "password": "Abcdefgh0"})
    second_company_token = response.json["access_token"]

    fake_update = {
        "id": current_job_id,
        "title": "Senior Software Engineer",
        "company": "Test Company",
        "location": "US",
        "industry": "Tech",
        "seniority": "Senior-Level"
    }

    response = client.put("/api/job_listings/", json=fake_update, headers={"Authorization": "Bearer " + second_company_token})
    assert response.status_code == 401 # nosec B101
    assert response.json == "You are not allowed to modify other company's job board" # nosec B101

    # Update the non-existing job listing
    nonexist_id = "650f78cda5b3b9cfa92d3b6e"
    nonexist_update = {
        "id": nonexist_id, # non-existing job id
        "title": "Senior Software Engineer",
        "company": "Test Company",
        "location": "US",
        "industry": "Tech",
        "seniority": "Senior-Level"
    }
    response = client.put("/api/job_listings/", json=nonexist_update, headers={"Authorization": "Bearer " + first_company_token})
    assert response.status_code == 404 # nosec B101
    assert response.json == "Cannot find the job you looking for" # nosec B101


    # Unauthorized access to delete job listings
    # Scenario 1: Job seeker tries to delete a job listing
    response = client.delete("/api/job_listings/12345", headers ={"Authorization": "Bearer " + job_seeker_token})
    assert response.status_code == 401 # nosec B101
    assert response.json == "Only companies can delete a job posting" # nosec B101
    # Scenario 2: Another company tries to delete your job listing
    response = client.delete(f"/api/job_listings/{current_job_id}", headers={"Authorization": f"Bearer {second_company_token}"})
    assert response.status_code == 401 # nosec B101
    assert response.json == "You are not allowed to modify other company's job board" # nosec B101

    # Delete the non-existing job listing
    response = client.delete(f"/api/job_listings/{nonexist_id}",  headers={"Authorization": "Bearer " + first_company_token})
    assert response.status_code == 404 # nosec B101
    assert response.json == "Cannot find the job you looking for" # nosec B101


    # Unauthorized access to get job listing applicant list
    # Scenario 1: Job seeker tries to get job listing applicant list
    response = client.get("/api/job_listings/12345/applicants", headers ={"Authorization": "Bearer " + job_seeker_token})
    assert response.status_code == 401 # nosec B101
    assert response.json == "Only companies can view applicants" # nosec B101
    # Scenario 2: Another company tries to get your job listing applicant list
    response = client.get(f"/api/job_listings/{current_job_id}/applicants", headers={"Authorization": f"Bearer {second_company_token}"})
    assert response.status_code == 401 # nosec B101
    assert response.json == "You are not allowed to view applicants from other company's job posting" # nosec B101

    # Get the non-existing job listing applicant list
    response = client.get(f"/api/job_listings/{nonexist_id}/applicants", headers={"Authorization": f"Bearer {first_company_token}"})
    assert response.status_code == 404 # nosec B101
    assert response.json == "Cannot find the job you looking for" # nosec B101

    # Unauthorized access to select job listing applicant 
    # Scenario: Job seeker tries to select job listing applicant
    # select_applicant = {
    #     "id": "12345",
    #     "applicant_email": "email@nyu.edu"
    # }
    # response = client.put("/job_listings/select", json=select_applicant, headers ={"Authorization": "Bearer " + job_seeker_token})
    # assert response.status_code == 401
    # assert response.json == "Only companies can select applicants"


def register_new_job(client):
    first_company = {
        "name": "Test Company",
        "email": "first_company@nyu.edu",
        "country": "US",
        "description": "ABC",
        "password": "Abcdefgh0"
    }

    new_job = {
        "title": "Software Engineer",
        "company": "Test Company",
        "location": "UAE",
        "industry": "Tech", 
        "seniority": "Mid-Level"
    }
    response = client.post("/api/companies/signup", json=first_company)
    response = client.post("/api/companies/login", json={"email": "first_company@nyu.edu", "password": "Abcdefgh0"})
    first_company_token = response.json["access_token"]

    response = client.post("/api/job_listings/", json=new_job, headers={"Authorization": "Bearer " + first_company_token})
    return response.json["job_id"]


def register_new_job_seeker(client):
    email = "johndoe@test.com"
    new_job_seeker = {
        "first": "John",
        "last": "Doe",
        "email": email,
        "expertise": "Software Engineering",
        "years": 3,
        "password": "SecurePass123"
    }
    response = client.post("/api/job_seekers/", json=new_job_seeker)
    response = client.post("/api/job_seekers/login", json={"email": email, "password": "SecurePass123"})
    job_seeker_token = response.json["access_token"]

    return email, job_seeker_token


def register_new_company(client):
    first_company = {
        "name": "Test Company",
        "email": "first_company@nyu.edu",
        "country": "US",
        "description": "ABC",
        "password": "Abcdefgh0"
    }

    response = client.post("/api/companies/signup", json=first_company)
    response = client.post("/api/companies/login", json={"email": "first_company@nyu.edu", "password": "Abcdefgh0"})
    first_company_token = response.json["access_token"]

    return first_company_token


def register_another_company(client):
    second_company = {
        "name": "Test Second Company",
        "email": "second_company@nyu.edu",
        "country": "US",
        "description": "ABC",
        "password": "Abcdefgh0"
    }

    response = client.post("/api/companies/signup", json=second_company)
    response = client.post("/api/companies/login", json={"email": "second_company@nyu.edu", "password": "Abcdefgh0"})
    second_company_token = response.json["access_token"]

    return second_company_token




def test_apply_job_scenario(client):
    # Applicants apply
    job_seeker_email, job_seeker_token = register_new_job_seeker(client)
    new_job_token = register_new_job(client)
    company_token = register_new_company(client)
    fake_job_token = "650f78cda5b3b9cfa92d3b6e"

    response = client.put(f"/api/job_listings/apply/{new_job_token}", headers={
        "Authorization": f"Bearer {job_seeker_token}"
    })

    assert response.status_code == 200 # nosec B101
    assert response.json == {'message': "Applied succesfully!"} # nosec B101

    # Failed scenarios:
    ## Scenario 1: Job seeker tries to apply for the same job again
    response = client.put(f"/api/job_listings/apply/{new_job_token}", headers={
        "Authorization": f"Bearer {job_seeker_token}"
    })

    assert response.status_code == 400 # nosec B101
    assert response.json == {'error': "You had applied for this position already!"} # nosec B101

    ## Scenario 2: Job seeker tries to apply for a non-existing job
    response = client.put(f"/api/job_listings/apply/{fake_job_token}", headers={
        "Authorization": f"Bearer {job_seeker_token}"
    })

    assert response.status_code == 404 # nosec B101
    assert response.json == {'error':"Cannot find the job you looking for"} # nosec B101

    ## Scenario 3: Company tries to apply for a job
    response = client.put(f"/api/job_listings/apply/{new_job_token}", headers={
        "Authorization": f"Bearer {company_token}"
    })

    assert response.status_code == 401 # nosec B101
    assert response.json == {'error':"Only signed-in job seekers can apply for job postings"} # nosec B101


def test_select_applicant_scenario(client):
    # Applicants apply
    job_seeker_email, job_seeker_token = register_new_job_seeker(client)
    new_job_token = register_new_job(client)
    company_token = register_new_company(client)
    fake_job_token = "650f78cda5b3b9cfa92d3b6e"

    response = client.put(f"/api/job_listings/apply/{new_job_token}", headers={
        "Authorization": f"Bearer {job_seeker_token}"
    })

    # Select applicant
    select_applicant = {
        "id": new_job_token,
        "email": job_seeker_email
    }

    response = client.get(f"/api/job_listings/{new_job_token}/applicants", headers={"Authorization": f"Bearer {company_token}"})

    response = client.put(f"/api/job_listings/select/accept", json=select_applicant, 
                           headers={"Authorization": f"Bearer {company_token}"})

    assert response.status_code == 200 # nosec B101
    assert response.json == "Selected succesfully!" # nosec B101

    # Applicant see their status updated
    response = client.get(f"/api/job_seekers/inquire", headers={"Authorization": f"Bearer {job_seeker_token}"})
    assert response.status_code == 200 # nosec B101
    # assert response.json['data'][new_job_token][0] == {'answer': 'Company name: Test Company. Position name: Software Engineer. Status: ACCEPTED /n '}
    assert response.json['data'][new_job_token][0] == "accepted" # nosec B101

    # Failed scenarios of selecting applicant
    ## Scenario 1: Job seeker tries to select an applicant
    response = client.put(f"/api/job_listings/select/accept", json=select_applicant,
                            headers={"Authorization": f"Bearer {job_seeker_token}"})
    assert response.status_code == 401 # nosec B101
    assert response.json == "Only companies can select applicants" # nosec B101
    ## Scenario 2: Another company tries to select an applicant
    second_company_token = register_another_company(client)
    response = client.put(f"/api/job_listings/select/accept", json=select_applicant,
                            headers={"Authorization": f"Bearer {second_company_token}"})
    assert response.status_code == 401 # nosec B101
    assert response.json == "You are not allowed to view applicants from other company's job posting!" # nosec B101
    ## Scenario 3: Company tries to select an applicant that is not applied
    select_applicant = {
        "id": new_job_token,
        "email": "nonexist@nyu.edu"}
    response = client.put(f"/api/job_listings/select/accept", json=select_applicant,
                            headers={"Authorization": f"Bearer {company_token}"})
    assert response.status_code == 404 # nosec B101
    assert response.json == "The applicant cannot be found on this job posting's applicant list!" # nosec B101
    ## Scenario 4: Company tries to select an applicant that is already selected
    select_applicant = {
        "id": new_job_token,
        "email": job_seeker_email
    }
    response = client.put(f"/api/job_listings/select/accept", json=select_applicant,
                            headers={"Authorization": f"Bearer {company_token}"})
    assert response.status_code == 404 # nosec B101
    assert response.json == "The applicant cannot be found on this job posting's applicant list!" # nosec B101
    ## Scenario 5: Company tries to select an applicant for a non-existing job
    select_applicant = {
        "id": fake_job_token,
        "email": job_seeker_email
    }
    response = client.put(f"/api/job_listings/select/accept", json=select_applicant,
                            headers={"Authorization": f"Bearer {company_token}"})
    assert response.status_code == 404 # nosec B101
    assert response.json == "Cannot find the job you looking for." # nosec B101
    ## Scenario 6: Not valid email format
    select_applicant = {
        "id": new_job_token,
        "email": "notvalid@"
    }
    response = client.put(f"/api/job_listings/select/accept", json=select_applicant,
                            headers={"Authorization": f"Bearer {company_token}"})
    assert response.status_code == 400 # nosec B101
    assert response.json == {"error": "Not appropriate email format"} # nosec B101


# Authentication test
def test_authentication(client):
    """
    Integration test to verify authentication
    """
    # 1. Sign up a company
    company_data = {
        "name": "Test Company",
        "email": "company@test.com",
        "country": "US",
        "description": "ABC",
        "password": "Abcdefgh0"
    }
    response = client.post("/api/companies/signup", json=company_data)
    assert response.status_code == 200 # nosec B101
    assert response.json["message"] == "Company Registered Successfully" # nosec B101

    # 2. Sign up a job seeker
    job_seeker_data = {
        "first": "Test Job Seeker",
        "last": "Test Job Seeker",
        "email": "jobseeker@test.com",
        "expertise": "CS",
        "years": 2,
        "password": "Abcdefgh0"
    }
    response = client.post("/api/job_seekers/signup", json=job_seeker_data)
    assert response.status_code == 200 # nosec B101
    assert response.json["message"] == "Job seeker Registered Successfully" # nosec B101

    # 3. Login as company
    login_data = {"email": "company@test.com", "password": "Abcdefgh0"}
    response = client.post("/api/companies/login", json=login_data)
    assert response.status_code == 200 # nosec B101
    company_token = response.json["access_token"]
    
    # 4. Login as job seeker
    login_data = {"email": "jobseeker@test.com", "password": "Abcdefgh0"}
    response = client.post("/api/job_seekers/login", json=login_data)
    assert response.status_code == 200 # nosec B101
    job_seeker_token = response.json["access_token"]

    # 5. Try accessing protected endpoints for companies without authentication
    response = client.get("/api/companies/find")
    assert response.status_code == 401 # nosec B101  # Unauthorized

    # 6. Access protected endpoint with authentication
    response = client.get("/api/companies/find", headers={"Authorization": f"Bearer {company_token}"})
    assert response.status_code == 200 # nosec B101  # Successful access

    # 7. Try accessing job_seeker protected endpoint without authentication
    response = client.get("/api/job_seekers/find")
    assert response.status_code == 401 # nosec B101  # Unauthorized

    # 8. Access job_seeker protected endpoint with authentication
    response = client.get("/api/job_seekers/find", headers={"Authorization": f"Bearer {job_seeker_token}"})
    assert response.status_code == 200 # nosec B101
    assert f"Hello {job_seeker_data['first']}" in response.json['message'] # nosec B101

    # 9. Try accessing job_seeker inquiry endpoint without authentication
    response = client.get("/api/job_seekers/inquire")
    assert response.status_code == 401 # nosec B101  # Unauthorized

    # 10. Access job_seeker inquiry endpoint with authentication
    response = client.get("/api/job_seekers/inquire", headers={"Authorization": f"Bearer {job_seeker_token}"})
    assert response.status_code == 200 # nosec B101
