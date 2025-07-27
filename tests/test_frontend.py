import dotenv
import os
from selenium.webdriver.common.by import By
import requests

dotenv.load_dotenv()
FRONTEND_URL = os.getenv("FRONTEND_URL")

# Test registration workflow
def test_job_seeker_registration(driver):
    # Navigate to the job seeker registration page
    driver.get(f"{FRONTEND_URL}/api/signup/job_seeker")
    assert driver.find_element(By.ID, "signup_title").text == "Join our job seeker community" # nosec B101

    # Get the inputs in the registration form
    first_name = driver.find_element(By.NAME, "first")
    last_name = driver.find_element(By.NAME, "last")
    email = driver.find_element(By.NAME, "email")
    password = driver.find_element(By.NAME, "password")
    expertise = driver.find_element(By.NAME, "expertise")
    year = driver.find_element(By.NAME, "year")
    submit = driver.find_element(By.ID, "signup_button")

    # Fill in the registration form
    first_name.send_keys("Foo")
    last_name.send_keys("Bar")
    email.send_keys("foobar@gmail.com")
    password.send_keys("Password123")
    expertise.send_keys("Programming, Flask")
    year.send_keys(1)

    # Submit the form
    submit.click()

    # Check if the job seeker is registered in the database
    response = requests.get(f"{FRONTEND_URL}/api/job_seekers/foobar@gmail.com", timeout=5)
    assert response.status_code == 200 # nosec B101


    
    
    
    
    