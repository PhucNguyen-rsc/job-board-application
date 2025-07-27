import dotenv
import pytest
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from conftest import driver
import pdb
import requests

dotenv.load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL")
FRONT_END_URL = os.getenv("FRONT_END_URL")


def test_unsigned_user_apply(driver):

    # Simulate where a user wants to access the only page to apply
    driver.get(FRONT_END_URL + "/jobs")
    
    assert "Access Denied" in driver.page_source # nosec B101
