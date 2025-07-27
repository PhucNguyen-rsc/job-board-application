import dotenv
import pytest
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import driver
import requests
from selenium.common.exceptions import NoSuchElementException

dotenv.load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL")
FRONT_END_URL = os.getenv("FRONT_END_URL")

print(BACKEND_URL)
print(FRONT_END_URL)

# Give a timeout for CI environments
DEFAULT_TIMEOUT = 20  # seconds



# --------------------------------------------------------------------------
# Registration and login tests


def test_register_as_company(driver):

    driver.get(FRONT_END_URL)
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located(
        (By.XPATH, '//h1[text()="Find Your Dream Job Today"]')
    ))

    sign_up_button = driver.find_element(By.XPATH,'//button[contains(text(), "Sign up")]')
    sign_up_button.click()
    
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.url_contains("/signup"))
    sign_up_as_company_button = driver.find_element(By.XPATH,'//button[text()="As Company"]')
    sign_up_as_company_button.click()
    
    # Fill in the registration form
    name = driver.find_element(By.NAME, "name")
    email = driver.find_element(By.NAME, "email")
    country = driver.find_element(By.NAME, "country")
    description = driver.find_element(By.NAME, "description")
    password = driver.find_element(By.NAME, "password")
    submit = driver.find_element(By.XPATH, '//button[text()="Create Account"]')
    
    # Submit the form
    name.send_keys("Testing Company")
    email.send_keys("test@example.com")
    country.send_keys("United Arab Emirates")
    description.send_keys("This is a testing company")
    password.send_keys("Password123")
    submit.click()
     
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'h1.text-green-600')
    ))
    
    assert "Account Created Successfully 🎉" in driver.page_source # nosec B101

    # Check if the job seeker is registered in the database
    response = requests.get(f"{BACKEND_URL}/companies/test@example.com")
    assert response.status_code == 200 # nosec B101

def test_login_as_company(driver):
    
    driver.get(FRONT_END_URL)

    driver.find_element(By.XPATH, '//button[text()="Log in"]').click()

    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.url_contains("/login"))

    driver.find_element(By.XPATH, '//button[text()="As Company"]').click()

    email = driver.find_element(By.XPATH, '//input[@name="email"]')
    password = driver.find_element(By.XPATH, '//input[@name="password"]')
    submit = driver.find_element(By.XPATH, '//button[text()="Sign In"]')

    # Test login failure
    email.send_keys("test@example.com")
    password.send_keys("Password1")
    submit.click()
    
    # WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Invalid")]')))
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.bg-red-100')))

    # Test login success

    email.clear()
    email.send_keys("test@example.com")
    password.clear()
    password.send_keys("Password123")
    submit.click()
    
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//h2[text()="Company Profile"]')))

    # Check if the company name and email match the registered data
    assert "Testing company" in driver.page_source # nosec B101
    assert "test@example.com" in driver.page_source # nosec B101
    

def test_register_as_job_seeker(driver):
    driver.get(FRONT_END_URL)
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//h1[text()="Find Your Dream Job Today"]')))

    sign_up_button = driver.find_element(By.XPATH,'//button[contains(text(), "Sign up")]')
    sign_up_button.click()

    
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.url_contains("/signup"))
    sign_up_as_company_button = driver.find_element(By.XPATH,'//button[text()="As Job Seeker"]')
    sign_up_as_company_button.click()
    
    # Fill in the registration form
    first = driver.find_element(By.NAME, "first")
    last = driver.find_element(By.NAME, "last")
    email = driver.find_element(By.NAME, "email")
    expertise = driver.find_element(By.NAME, "expertise")
    years = driver.find_element(By.NAME, "years")
    password = driver.find_element(By.NAME, "password")
    submit = driver.find_element(By.XPATH, '//button[text()="Create Account"]')
    
    # Submit the form
    first.send_keys("Test")
    last.send_keys("Seeker")
    email.send_keys("tester@seeker.com")
    expertise.send_keys("CS")
    years.send_keys(3)
    password.send_keys("Password123")
    submit.click()
     
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located(
        (By.XPATH, '//h1[text()="Account Created Successfully 🎉"]')
    ))

    # Check if the job seeker is registered in the database
    response = requests.get(f"{BACKEND_URL}/job_seekers/tester@seeker.com")
    assert response.status_code == 200 # nosec B101



def test_register_fail_as_job_seeker(driver):
    driver.get(FRONT_END_URL)
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//h1[text()="Find Your Dream Job Today"]')))

    sign_up_button = driver.find_element(By.XPATH,'//button[contains(text(), "Sign up")]')
    sign_up_button.click()
    
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.url_contains("/signup"))
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//button[text()="As Job Seeker"]')))
    sign_up_as_company_button = driver.find_element(By.XPATH,'//button[text()="As Job Seeker"]')
    sign_up_as_company_button.click()
    
    first = driver.find_element(By.NAME, "first")
    last = driver.find_element(By.NAME, "last")
    email = driver.find_element(By.NAME, "email")
    expertise = driver.find_element(By.NAME, "expertise")
    years = driver.find_element(By.NAME, "years")
    password = driver.find_element(By.NAME, "password")
    submit = driver.find_element(By.XPATH, '//button[text()="Create Account"]')

    first.send_keys("Wrong")
    last.send_keys("Input")
    email.send_keys("not_valid_email")
    expertise.send_keys("CS")
    years.send_keys(3)
    password.send_keys("somePassword123")
    submit.click()

    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//div[contains(string(.), "Invalid Email Format!")]')))


def test_login_fail_as_job_seeker(driver):
    driver.get(FRONT_END_URL)
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//h1[text()="Find Your Dream Job Today"]')))

    driver.find_element(By.XPATH, '//button[text()="Log in"]').click()

    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.url_contains("/login"))
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//button[text()="As Job Seeker"]')))

    driver.find_element(By.XPATH, '//button[text()="As Job Seeker"]').click()

    email = driver.find_element(By.XPATH, '//input[@name="email"]')
    password = driver.find_element(By.XPATH, '//input[@name="password"]')
    submit = driver.find_element(By.XPATH, '//button[text()="Sign In"]')

    email.send_keys("wrong_email@test.com")
    password.send_keys("WrongPassword123")
    submit.click()

    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//div[contains(string(.), "Invalid Credentials!")]')))



def test_login_as_job_seeker(driver):
    driver.get(FRONT_END_URL)
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//h1[text()="Find Your Dream Job Today"]')))

    # Click on the login button
    driver.find_element(By.XPATH, '//button[text()="Log in"]').click()

    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.url_contains("/login"))

    # Click on the job seeker button
    driver.find_element(By.XPATH, '//button[text()="As Job Seeker"]').click()

    email = driver.find_element(By.XPATH, '//input[@name="email"]')
    password = driver.find_element(By.XPATH, '//input[@name="password"]')
    submit = driver.find_element(By.XPATH, '//button[text()="Sign In"]')

    email.send_keys("tester@seeker.com")
    password.send_keys("Password123")
    submit.click()
    
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.url_contains("/jobs"))

    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//h2[text()="Profile Information"]')))

    # Check if the job seeker name and email match the registered data
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//p[contains(string(.), "Test Seeker")]')))
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//p[contains(string(.), "tester@seeker.com")]')))



# --------------------------------------------------------------------
# Workflow testing



def test_company_post_job_listing_fail(driver):
    # Login as company
    driver.get(FRONT_END_URL + "/login")
    driver.find_element(By.XPATH, '//button[text()="As Company"]').click()

    email = driver.find_element(By.XPATH, '//input[@name="email"]')
    password = driver.find_element(By.XPATH, '//input[@name="password"]')
    submit = driver.find_element(By.XPATH, '//button[text()="Sign In"]')

    email.send_keys("test@example.com")
    password.send_keys("Password123")
    submit.click()
    
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//p[text()="Testing company"]')))

    # Click post new job button
    driver.find_element(By.XPATH, '//button[text()="Post New Job"]').click()

    # Fill in the job posting form with invalid data
    title = driver.find_element(By.NAME, "title")
    location = driver.find_element(By.NAME, "location")
    industry = driver.find_element(By.NAME, "industry")
    seniority = driver.find_element(By.NAME, "seniority")
    submit = driver.find_element(By.XPATH, '//button[text()="Post Job"]')

    # Submit empty form
    submit.click()

    # Wait for error message
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//div[contains(string(.), "Please fill in all fields")]')))

def test_company_post_job_listing(driver):
    # Login as company
    driver.get(FRONT_END_URL + "/login")
    driver.find_element(By.XPATH, '//button[text()="As Company"]').click()

    email = driver.find_element(By.XPATH, '//input[@name="email"]')
    password = driver.find_element(By.XPATH, '//input[@name="password"]')
    submit = driver.find_element(By.XPATH, '//button[text()="Sign In"]')

    email.send_keys("test@example.com")
    password.send_keys("Password123")
    submit.click()
    
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//p[text()="Testing company"]')))

    # Click post new job button
    driver.find_element(By.XPATH, '//button[text()="Post New Job"]').click()

    # Fill in the job posting form
    title = driver.find_element(By.NAME, "title")
    location = driver.find_element(By.NAME, "location")
    industry = driver.find_element(By.NAME, "industry")
    seniority = driver.find_element(By.NAME, "seniority")
    submit = driver.find_element(By.XPATH, '//button[text()="Post Job"]')

    title.send_keys("Software Engineer")
    location.send_keys("New York")
    industry.send_keys("Technology")
    seniority.send_keys("Mid-Level")
    submit.click()

    # Wait for success message
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//div[contains(string(.), "Job posted successfully")]')))

def test_unsigned_user_search_job(driver):
    driver.get(FRONT_END_URL)
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//h1[text()="Find Your Dream Job Today"]')))

    # Search for jobs
    search = driver.find_element(By.NAME, "search")
    search.send_keys("Software Engineer")
    search.submit()

    # Wait for search results
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "job-listing")]')))

    # Try to apply for a job (should be redirected to login)
    driver.find_element(By.XPATH, '//button[text()="Apply"]').click()
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.url_contains("/login"))

def test_job_seeker_search_and_apply_jobs(driver):
    # Login as job seeker
    driver.get(FRONT_END_URL + "/login")
    driver.find_element(By.XPATH, '//button[text()="As Job Seeker"]').click()

    email = driver.find_element(By.XPATH, '//input[@name="email"]')
    password = driver.find_element(By.XPATH, '//input[@name="password"]')
    submit = driver.find_element(By.XPATH, '//button[text()="Sign In"]')

    email.send_keys("tester@seeker.com")
    password.send_keys("Password123")
    submit.click()

    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.url_contains("/jobs"))

    # Search for jobs
    search = driver.find_element(By.NAME, "search")
    search.send_keys("Software Engineer")
    search.submit()

    # Wait for search results
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "job-listing")]')))

    # Apply for a job
    driver.find_element(By.XPATH, '//button[text()="Apply"]').click()

    # Wait for success message
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//div[contains(string(.), "Application submitted successfully")]')))

    # Try to apply again (should show error)
    driver.find_element(By.XPATH, '//button[text()="Apply"]').click()
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//div[contains(string(.), "You have already applied to this job")]')))

def test_company_get_applicants(driver):
    
    # Login as a company
    driver.get(FRONT_END_URL + "/login")
    driver.find_element(By.XPATH, '//button[text()="As Company"]').click()

    email = driver.find_element(By.XPATH, '//input[@name="email"]')
    password = driver.find_element(By.XPATH, '//input[@name="password"]')
    submit = driver.find_element(By.XPATH, '//button[text()="Sign In"]')

    email.send_keys("test@example.com")
    password.send_keys("Password123")
    submit.click()

    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//p[text()="Testing company"]')))

    # View job listings
    driver.find_element(By.XPATH, '//button[text()="View Job Listings"]').click()

    # Wait for job listings to load
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "job-listing")]')))

    # View applicants for a job
    driver.find_element(By.XPATH, '//button[text()="View Applicants"]').click()

    # Wait for applicants list to load
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "applicant")]')))

def test_company_select_applicants(driver):
    
    # Login as a company 
    driver.get(FRONT_END_URL + "/login")
    driver.find_element(By.XPATH, '//button[text()="As Company"]').click()

    email = driver.find_element(By.XPATH, '//input[@name="email"]')
    password = driver.find_element(By.XPATH, '//input[@name="password"]')
    submit = driver.find_element(By.XPATH, '//button[text()="Sign In"]')

    email.send_keys("test@example.com")
    password.send_keys("Password123")
    submit.click()

    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//p[text()="Testing company"]')))

    # View job listings
    driver.find_element(By.XPATH, '//button[text()="View Job Listings"]').click()

    # Wait for job listings to load
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "job-listing")]')))

    # View applicants for a job
    driver.find_element(By.XPATH, '//button[text()="View Applicants"]').click()

    # Wait for applicants list to load
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "applicant")]')))

    # Select an applicant
    driver.find_element(By.XPATH, '//button[text()="Select"]').click()

    # Wait for success message
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//div[contains(string(.), "Applicant selected successfully")]')))

def test_company_delete_job_listing(driver):
    # Login as company
    driver.get(FRONT_END_URL + "/login")
    driver.find_element(By.XPATH, '//button[text()="As Company"]').click()

    email = driver.find_element(By.XPATH, '//input[@name="email"]')
    password = driver.find_element(By.XPATH, '//input[@name="password"]')
    submit = driver.find_element(By.XPATH, '//button[text()="Sign In"]')

    email.send_keys("test@example.com")
    password.send_keys("Password123")
    submit.click()

    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//p[text()="Testing company"]')))

    # View job listings
    driver.find_element(By.XPATH, '//button[text()="View Job Listings"]').click()

    # Wait for job listings to load
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "job-listing")]')))

    # Delete a job listing
    driver.find_element(By.XPATH, '//button[text()="Delete"]').click()

    # Wait for success message
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//div[contains(string(.), "Job listing deleted successfully")]')))