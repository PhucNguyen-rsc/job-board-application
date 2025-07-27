from abc import ABC
from os import environ
from dotenv import load_dotenv
import mongomock
import pymongo
import os
from pymongo import MongoClient


# Load environment variables from .env file
load_dotenv()

class BaseConfig(ABC):
    DEBUG = False
    TESTING = False
    DB_CLIENT = lambda uri: pymongo.MongoClient(uri)

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    MONGO_URI = environ.get('DEV_MONGODB_URI')
    DB_NAME = environ.get('DEV_DB_NAME')
    MONGO_DB_USERNAME = environ.get('MONGO_DB_USERNAME')
    MONGO_DB_PASSWORD = environ.get('MONGO_DB_PASSWORD')
    IS_PROD = environ.get('IS_PROD')
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')

class ProductionConfig(BaseConfig):
    MONGO_URI = environ.get('PROD_MONGODB_URI')
    DB_NAME = environ.get('PROD_DB_NAME')
    MONGO_DB_USERNAME = environ.get('MONGO_DB_USERNAME')
    MONGO_DB_PASSWORD = environ.get('MONGO_DB_PASSWORD')
    IS_PROD = environ.get('IS_PROD')

class UnitTestConfig(BaseConfig):
    """
    Use mongomock for unit tests.
    """
    TESTING = True
    MONGO_URI = environ.get('UNIT_TEST_MONGODB_URI')
    DB_NAME = environ.get('TEST_DB_NAME')
    MONGO_DB_USERNAME = environ.get('MONGO_DB_USERNAME')
    MONGO_DB_PASSWORD = environ.get('MONGO_DB_PASSWORD')
    IS_PROD = environ.get('IS_PROD')
    DB_CLIENT = lambda uri: mongomock.MongoClient(uri)

# app/config.py

class IntegrationTestConfig:
    TESTING = True
    DB_CLIENT = MongoClient
    MONGO_URI = environ.get("INTEGRATION_TEST_MONGODB_URI")
    DB_NAME = environ.get("TEST_DB_NAME")
    MONGO_DB_USERNAME = environ.get('MONGO_DB_USERNAME')
    MONGO_DB_PASSWORD = environ.get('MONGO_DB_PASSWORD')
    IS_PROD = environ.get('IS_PROD')
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY', 'my_super_secret_key')



