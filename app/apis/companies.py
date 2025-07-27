from flask_restx import Namespace, Resource, fields
from ..db import companies
from http import HTTPStatus
from flask import request
from bson.json_util import dumps
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, current_user

from datetime import timedelta
from .utils import validate_email, is_valid_password  # validate emails and passwords

authorizations = {
    "apikey": {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Namespace("companies", description="Endpoint for companies API", authorizations=authorizations)

COMPANY_CREATE_FLDS = api.model(
    "AddCompanyEntry",
    {
        companies.NAME: fields.String,
        companies.COMPANY_EMAIL: fields.String,
        companies.COUNTRY: fields.String,
        companies.DESCRIPTION: fields.String,
        companies.PASSWORD: fields.String
    },
)

COMPANY_LOGIN_FLDS = api.model(
    "LoginCompanyEntry",
    {
        companies.COMPANY_EMAIL: fields.String,
        companies.PASSWORD: fields.String
    }
)


@api.route("/") 
@api.response(HTTPStatus.OK, "Success")
@api.response(404, "Company not found")
@api.response(HTTPStatus.CONFLICT, "Email already exists")
class CompanyList(Resource):
    @api.doc("List all companies")
    def get(self):
        company_list = companies.get_companies()
        if company_list:
            # Hide passwords before returning
            for c in company_list:
                c.pop("password", None)
            return company_list, HTTPStatus.OK
        else:
            return "Not found", HTTPStatus.NOT_FOUND

    @api.expect(COMPANY_CREATE_FLDS)
    def post(self):
        name = request.json.get(companies.NAME)
        email = request.json.get(companies.COMPANY_EMAIL)
        country = request.json.get(companies.COUNTRY)
        description = request.json.get(companies.DESCRIPTION)
        password = request.json.get(companies.PASSWORD)

        # Validate email
        if not validate_email(email):
            return {"error": "Not appropriate email format"}, 400

        # Check if company email already exists
        record = companies.find_company(email)
        if record:
            return {"error": "The email address already exists"}, HTTPStatus.CONFLICT

        # Create the new company
        company_id = companies.create_company(name, email, country, description, password)
        print(f"Created company with id: {company_id}")
        # Return a dict so Flask-RESTX can handle JSON
        return {"message": "Company created"}, HTTPStatus.OK


@api.route("/<email>")
@api.param("email", "Company email to use for lookup")
@api.response(HTTPStatus.OK, "Success")
@api.response(HTTPStatus.NOT_ACCEPTABLE, "Not acceptable")
@api.response(404, "Company not found")
@api.response(HTTPStatus.CONFLICT, "Email already exists")
class Company(Resource):
    @api.doc("Filter company by its email")
    def get(self, email):
        if not validate_email(email):
            return {"error": "Not appropriate email format"}, 400

        company = companies.find_company(email)
        if company:
            # Hide the password
            company.pop("password", None)
            return company, HTTPStatus.OK
        else:
            return "Not found", HTTPStatus.NOT_FOUND

    @api.expect(COMPANY_CREATE_FLDS)
    @api.doc("Update a specific company, identified by email")
    def put(self, email):
        if not validate_email(email):
            return {"error": "Not appropriate email format"}, 400

        name = request.json.get(companies.NAME)
        new_email = request.json.get(companies.COMPANY_EMAIL)
        country = request.json.get(companies.COUNTRY)
        description = request.json.get(companies.DESCRIPTION)

        updated_company = companies.update_company(email, name, new_email, country, description)
        if updated_company is None:
            return "Company email not found", HTTPStatus.NOT_FOUND

        return "Company updated", HTTPStatus.OK

    @api.doc("Delete a specific company, identified by email")
    def delete(self, email):
        if not validate_email(email):
            return {"error": "Not appropriate email format"}, 400

        delete_company = companies.delete_company(email)
        if delete_company is None:
            return "Company email not found", HTTPStatus.NOT_FOUND

        return "Company deleted", HTTPStatus.OK


@api.route("/login")
@api.response(HTTPStatus.OK, "Success")
@api.response(HTTPStatus.NOT_ACCEPTABLE, "Not acceptable")
class Company(Resource):
    @api.expect(COMPANY_LOGIN_FLDS)
    @api.doc("Login a company")
    def post(self):
        email = request.json.get(companies.COMPANY_EMAIL)
        password = request.json.get(companies.PASSWORD)

        if not validate_email(email):
            return {"error": "Not appropriate email format"}, 400

        userEntry = companies.find_company(email)
        if userEntry and companies.check_login_credentials(email, password):
            access_token = create_access_token(
                identity=userEntry, expires_delta=timedelta(hours=0.5)
            )
            return {
                "message": "Logged in Successfully",
                "access_token": access_token
            }, HTTPStatus.OK

        return {"error":"Bad credentials"}, HTTPStatus.UNAUTHORIZED


@api.route("/signup")
@api.response(HTTPStatus.OK, "Success")
@api.response(HTTPStatus.CONFLICT, "Email already exists")
@api.response(HTTPStatus.CONFLICT, "Company name already exists")  # new
class Company(Resource):
    @api.expect(COMPANY_CREATE_FLDS)
    @api.doc("Sign up a company")
    def post(self):
        name = request.json.get(companies.NAME)
        email = request.json.get(companies.COMPANY_EMAIL)
        country = request.json.get(companies.COUNTRY)
        description = request.json.get(companies.DESCRIPTION)
        password = request.json.get(companies.PASSWORD)

        # Validate email
        if not validate_email(email):
            return {"error": "Not appropriate email format"}, 400

        # Validate password strength
        if not is_valid_password(password):
            return {"error": "Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, and a number"}, 400

        # Check for duplicate email
        if companies.find_company(email):
            return {"error": "The email address already exists"}, HTTPStatus.CONFLICT

        # Check for duplicate company name
        if companies.find_company_by_name(name):  
            return {"error": "The company name already exists"}, HTTPStatus.CONFLICT

        # Create the company
        company_id = companies.create_company(name, email, country, description, password)
        print(f"Created company with id: {company_id}")
        return {"message": "Company Registered Successfully"}, HTTPStatus.OK


@api.route("/find")
@api.response(HTTPStatus.OK, "Success")
class Company(Resource):
    @api.doc("Testing functionality of JWT")
    @api.doc(security='apikey')
    @jwt_required()
    def get(self):
        print("current_user", current_user)
        if "name" not in current_user:
            return {"error":"Only companies are allowed to do this action"}, 401
        return {"message": f"Logged in as {current_user['name']}"},200
