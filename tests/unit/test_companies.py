from .utils import assert_items_equal


def test_list_companies_count(client, companies):
    """
    Test that the number of companies returned by the /companies/ endpoint matches the seeded data.
    """
    response = client.get("/api/companies/")
    assert response.status_code == 200 # nosec B101

    data = response.json
    assert isinstance(data, list) # nosec B101
    assert len(data) == len(companies) # nosec B101


def test_companies_match_seed_data(client, single_company):
    """
    Test that a single seeded company is returned by the companies/ endpoint and matches the seed data.
    """
    response = client.get("/api/companies/")
    assert response.status_code == 200 # nosec B101

    data = response.json
    assert isinstance(data, list) # nosec B101

    data_dict = {s["email"]: s for s in data}
    assert single_company["email"] in data_dict, f"Company with email {single_company['email']} not found in response." # nosec B101

    retrieved_company = data_dict[single_company["email"]]
    assert retrieved_company["name"] == single_company["name"], f"Mismatch in 'name' for {single_company['email']}" # nosec B101
    assert retrieved_company["email"] == single_company["email"], f"Mismatch in 'email' for {single_company['email']}" # nosec B101
    assert retrieved_company["country"] == single_company["country"], f"Mismatch in 'country' for {single_company['email']}" # nosec B101
    assert retrieved_company["description"] == single_company["description"], f"Mismatch in 'description' for {single_company['email']}" # nosec B101


def test_get_existing_company(client):
    response = client.get("/api/companies/app@apple.com")
    assert response.status_code == 200 # nosec B101
    assert_items_equal(response.json, {
        "name": "Apple",
        "email": "app@apple.com",
        "country": "United States",
        "description": "IT company"
    }) # nosec B101


def test_get_non_existing_company(client):
    response = client.get("/api/companies/non_existent@nyu.edu")
    assert response.status_code == 404 # nosec B101
    assert response.json == "Not found" # nosec B101


def test_create_company(client):
    new_company = {"name": "john", "email": "john@nyu.edu", "country": "korea", "description": "good"}

    response = client.post("/api/companies/", json=new_company)
    assert response.status_code == 200 # nosec B101
    
    # Expecting a JSON dict with {"message": "..."}
    resp_json = response.get_json()
    assert isinstance(resp_json, dict) # nosec B101
    assert resp_json["message"] == "Company created" # nosec B101

    # Check that the company was actually created
    response = client.get("/api/companies/john@nyu.edu")
    assert response.status_code == 200 # nosec B101
    assert_items_equal(response.json, new_company) # nosec B101


def test_update_company(client):
    company_email = "app@nvidia.com"
    updated_company = {
        "name": "new_NVIDIA",
        "email": company_email,
        "country": "US",
        "description": "Very sad"
    }
    response = client.put(f"/api/companies/{company_email}", json=updated_company)
    assert response.status_code == 200 # nosec B101
    assert response.json == "Company updated" # nosec B101

    # Check that the student was actually updated
    response = client.get(f"/api/companies/{company_email}")
    assert response.status_code == 200 # nosec B101
    assert_items_equal(response.json, updated_company) # nosec B101


def test_update_non_existing_company(client):
    company_email = "nonexistent@nyu.edu"
    updated_company = {
        "name": "Nonexistent",
        "email": company_email,
        "country": "China",
        "description": "freshman student company"
    }
    response = client.put(f"/api/companies/{company_email}", json=updated_company)
    assert response.status_code == 404 # nosec B101
    assert response.json == "Company email not found" # nosec B101

    # Check that the company was not created
    response = client.get(f"/api/companies/{company_email}")
    assert response.status_code == 404 # nosec B101

def test_delete_company(client):
    company_email = "app@apple.com"
    response = client.delete(f"/api/companies/{company_email}")
    assert response.status_code == 200 # nosec B101

    response = client.get(f"/api/companies/{company_email}")
    assert response.status_code == 404 # nosec B101

def test_get_empty_company_list(client, clear_company_db):
    response = client.get("/api/companies/")
    assert response.status_code == 404 # nosec B101

def test_invalid_email(client):
    invalid_email = "invalid@"
    valid_email = "valid@gmail.com"

    new_company = {
        "name": "Nonexistent",
        "email": invalid_email,
        "country": "China",
        "description": "freshman student company"
    }
    new_login = { #wrong email format for sign in and sign up
        "email": invalid_email,
        "password": "12345"
    }

    new_signup = { #testing for wrong passport format
        "email": valid_email,
        "password": "12", # bad password
        "name": "Nonexistent",
        "country": "China",
        "description": "fake company"
    }

    # invalid email input in the post request in companies/ endpoint
    response = client.post(f"/api/companies/", json=new_company)
    assert response.status_code == 400 # nosec B101
    assert response.json ==  {'error': 'Not appropriate email format'} # nosec B101

    # invalid email input in the get request in companies/<email> endpoint
    response = client.get(f"/api/companies/{invalid_email}", json=new_company)
    assert response.status_code == 400 # nosec B101
    assert response.json ==  {'error': 'Not appropriate email format'} # nosec B101

    response = client.put(f"/api/companies/{invalid_email}", json=new_company)
    assert response.status_code == 400 # nosec B101
    assert response.json ==  {'error': 'Not appropriate email format'} # nosec B101

    response = client.delete(f"/api/companies/{invalid_email}")
    assert response.status_code == 400 # nosec B101
    assert response.json ==  {'error': 'Not appropriate email format'} # nosec B101

    response = client.post(f"/api/companies/login", json=new_login)
    assert response.status_code == 400 # nosec B101
    assert response.json ==  {'error': 'Not appropriate email format'} # nosec B101


    response = client.post(f"/api/companies/signup", json=new_login)
    assert response.status_code == 400 # nosec B101
    assert response.json ==  {'error': 'Not appropriate email format'} # nosec B101

    response = client.post(f"/api/companies/signup", json=new_signup)
    assert response.status_code == 400 # nosec B101
    assert response.json ==  {"error": "Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, and a number"} # nosec B101



