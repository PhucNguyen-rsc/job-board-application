from tests.unit.utils import assert_items_equal
from app.db.utils import is_valid_email
import unittest

def test_list_seekers_count(client, job_seekers):
    """
    Test that the number of job_seekers returned by the job_seekers/ endpoint matches the seeded data.
    """
    response = client.get("/api/job_seekers/")
    assert response.status_code == 200 # nosec B101

    data = response.json
    assert isinstance(data, list) # nosec B101
    assert len(data) == len(job_seekers) # nosec B101

def test_get_existing_seeker(client):
    response = client.get("/api/job_seekers/jd@gmail.com")
    assert response.status_code == 200 # nosec B101
    assert_items_equal(response.json, {
        "first": "John",
        "last": "Doe",
        "email": "jd@gmail.com",
        "expertise": "Programming",
        "years": 12
    })

def test_get_non_existing_seeker(client):
    response = client.get("/api/job_seekers/non_existent@gmail.com")
    assert response.status_code == 404 # nosec B101
    assert response.json == "Not found" # nosec B101

def test_create_seeker(client):
    new_seeker = {
        "first": "Foo",
        "last": "Bar",
        "email": "foobar@gmail.com",
        "expertise": "Programming, Flask",
        "years": 1
    }

    response = client.post("/api/job_seekers/", json=new_seeker)
    assert response.status_code == 200 # nosec B101

    resp_json = response.get_json()
    assert resp_json["message"] == "Job seeker created" # nosec B101

    # Now check the newly created seeker
    response = client.get("/api/job_seekers/foobar@gmail.com")
    assert response.status_code == 200 # nosec B101

    # Exclude "_id", "accepted", "applied" from the comparison
    assert_items_equal(
        response.json,
        new_seeker,
        extra_exclude={"_id", "accepted", "applied", "password"}
    )

def test_create_duplicate_seeker(client):
    duplicate_seeker = {
        "first": "Jason",
        "second": "Aplin",
        "email": "jap@gmail.com",
        "expertise": "Performance Analysis",
        "years": 19
    }

    response = client.post("/api/job_seekers/", json=duplicate_seeker)
    assert response.status_code == 409 # nosec B101

    # Expecting a JSON dict with {"error": "..."}
    resp_json = response.get_json()
    assert isinstance(resp_json, dict) # nosec B101
    assert resp_json["error"] == "The email address already exists" # nosec B101

    # Check that the existing user was NOT overwritten
    response = client.get("/api/job_seekers/jap@gmail.com")
    assert_items_equal(response.json, {
        "first": "Jon",
        "last": "Appleseed",
        "email": "jap@gmail.com",
        "expertise": "Computer Security",
        "years": 7
    })

def test_update_seeker(client):
    seeker_email = "ab@gmail.com"
    updated_seeker = {
        "first": "Alice",
        "last": "Bob",
        "email": seeker_email,
        "expertise": "Finance",
        "years": 11
    }
    response = client.put(f"/api/job_seekers/{seeker_email}", json=updated_seeker)
    assert response.status_code == 200 # nosec B101
    assert response.json == "Job seeker updated" # nosec B101

    # Check that the seeker was actually updated
    response = client.get(f"/api/job_seekers/{seeker_email}")
    assert response.status_code == 200 # nosec B101
    assert_items_equal(response.json, updated_seeker)

def test_update_non_existing_seeker(client):
    seeker_email = "nonexistent@nyu.edu"
    updated_seeker = {
        "first": "Nonexistent",
        "last": "Person",
        "email": seeker_email,
        "expertise": "None",
        "years": 0
    }
    response = client.put(f"/api/job_seekers/{seeker_email}", json=updated_seeker)
    assert response.status_code == 404 # nosec B101
    assert response.json == "Job seeker email not found" # nosec B101

    # Check that the seeker was not created
    response = client.get(f"/api/job_seekers/{seeker_email}")
    assert response.status_code == 404 # nosec B101

def test_delete_seeker(client):
    seeker_email = "ab@gmail.com"
    response = client.delete(f"/api/job_seekers/{seeker_email}")
    assert response.status_code == 200 # nosec B101
    assert response.json == "Job seeker deleted" # nosec B101

    # Check that the seeker was deleted
    response = client.get(f"/api/job_seekers/{seeker_email}")
    assert response.status_code == 404 # nosec B101

def test_delete_non_existing_seeker(client):
    seeker_email = "nonexistent@gmail.com"
    response = client.delete(f"/api/job_seekers/{seeker_email}")
    assert response.status_code == 404 # nosec B101
    assert response.json == "Job seeker email not found" # nosec B101

class TestEmailValidation(unittest.TestCase):
    def test_valid_emails(self):
        self.assertTrue(is_valid_email("test@gmail.com")) # nosec B101
        self.assertTrue(is_valid_email("user@company.com")) # nosec B101
        self.assertTrue(is_valid_email("name@co.uk")) # nosec B101
        self.assertTrue(is_valid_email("user123@example.org")) # nosec B101

    def test_invalid_emails(self):
        self.assertFalse(is_valid_email("invalidemail.com")) # nosec B101
        self.assertFalse(is_valid_email("user@domain")) # nosec B101
        self.assertFalse(is_valid_email("user@@domain.com")) # nosec B101
        self.assertFalse(is_valid_email("user@.com")) # nosec B101
        self.assertFalse(is_valid_email("user@domain..com")) # nosec B101
        self.assertFalse(is_valid_email("")) # nosec B101
        self.assertFalse(is_valid_email()) # nosec B101

def test_invalid_email(client):
    invalid_email = "invalid@"
    valid_email = "valid@gmail.com"

    new_job_seeker = {
        "first": "Phuc",
        "last": "Nguyen",
        "email": invalid_email,
        "expertise": "CS",
        "years": 1,
        "password": "12345678"
    }

    new_login = { # wrong email format for sign in and sign up
        "email": invalid_email,
        "password": "12345"
    }

    new_signup = { #testing for wrong passport format
        "first": "Phuc",
        "last": "Nguyen",
        "email": valid_email,
        "expertise": "CS",
        "years": 1,
        "password": "123"
    }

    # invalid email input in the post request in job_seekr/ endpoint
    response = client.post(f"/api/job_seekers/", json=new_job_seeker)
    assert response.status_code == 400 # nosec B101
    assert response.json ==  {"error": "Invalid email format"} # nosec B101

    # invalid email input in the get request in companies/<email> endpoint
    response = client.get(f"/api/job_seekers/{invalid_email}", json=new_job_seeker)
    assert response.status_code == 400 # nosec B101
    assert response.json ==  {"error": "Invalid email format"} # nosec B101

    response = client.put(f"/api/job_seekers/{invalid_email}", json=new_job_seeker)
    assert response.status_code == 400 # nosec B101
    assert response.json ==  'Not approriate email format' # nosec B101

    response = client.delete(f"/api/job_seekers/{invalid_email}")
    assert response.status_code == 400 # nosec B101
    assert response.json ==  'Not approriate email format' # nosec B101

    response = client.post(f"/api/job_seekers/login", json=new_login)
    assert response.status_code == 400 # nosec B101
    assert response.json ==  "Not approriate email format" # nosec B101

    response = client.post(f"/api/job_seekers/signup", json=new_login)
    assert response.status_code == 400 # nosec B101
    assert response.json ==  "Not approriate email format" # nosec B101

    response = client.post(f"/api/job_seekers/signup", json=new_signup)
    assert response.status_code == 400 # nosec B101
    assert response.json ==  "Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, and a number" # nosec B101

