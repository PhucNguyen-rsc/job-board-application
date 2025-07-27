import pytest
import yaml

# Set up to import from the parent directory (/app)
# import os
# import sys
# child_dir = os.path.dirname(__file__)
# parent_dir = os.path.abspath(os.path.join(child_dir, '..'))
# sys.path.append(parent_dir)

from app import create_app
from app.config import UnitTestConfig
from app.db.db import get_collection


@pytest.fixture(scope='session')
def app():
    from app.config import IntegrationTestConfig
    app = create_app(IntegrationTestConfig)  # this already calls init_db inside create_app
    yield app


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def runner(app):
    return app.test_cli_runner()


def load_job_seekers():
    """
    Load job seekers data from the YAML fixture file.
    """
    with open("tests/unit/fixtures/job_seekers.yaml", "r") as file:
        job_seekers = yaml.safe_load(file)

    return job_seekers


@pytest.fixture(scope='session')
def job_seekers():
    return load_job_seekers()


@pytest.fixture(scope='function', autouse=True)
def seeded_job_seekers_db(job_seekers):
    """
    Preload the mock 'job_seekers' collection with data from the YAML fixture.
    """
    collection = get_collection("job_seekers")
    collection.delete_many({})  # Clear existing data
    collection.insert_many(job_seekers)


@pytest.fixture(scope='function', params=load_job_seekers())
def single_seeker(request):
    return request.param


def load_companies():
    """
    Load companies data from the YAML fixture file.
    """
    with open("tests/unit/fixtures/companies.yaml", "r") as file:
        companies = yaml.safe_load(file)

    return companies


@pytest.fixture(scope='session')
def companies():
    return load_companies()


@pytest.fixture(scope='function', autouse=True)
def seeded_companies_db(companies):
    """
    Preload the mock 'companies' collection with data from the YAML fixture.
    """
    collection = get_collection("companies")
    collection.delete_many({})  # Clear existing data
    collection.insert_many(companies)


@pytest.fixture(scope='function', params=load_companies())
def single_company(request):
    return request.param

@pytest.fixture(scope='function')
def clear_company_db():
    collection = get_collection("companies")
    collection.delete_many({})  # Clear existing data
    