# app/__init__.py
from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_talisman import Talisman
import flask
# Import your config(s)
from app.config import DevelopmentConfig

# Import the MongoDB initialization functions
from app.db.db import init_db
from app.db import job_seekers as job_seekers_db
from app.db import companies as companies_db

# Import your Flask-RESTX namespaces
from app.apis.job_seekers import api as job_seekers_ns
from app.apis.companies import api as companies_ns
from app.apis.job_listings import api as job_listings_ns

import os

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.secret_key = os.environ.get("BACKEND_SECRET_KEY")
    # Secure the app with Talisman
    is_dev = app.config.get("ENV") == "development" or os.environ.get("FLASK_ENV") == "development"

    # 🔒 Secure Headers for CSP / ZAP (only in development)
    if is_dev:
        
        Talisman(app,
            content_security_policy={
                "default-src": "'self'",
                "script-src": "'self' 'unsafe-inline'",
                "style-src": "'self' 'unsafe-inline'",
                "img-src": "'self' data:",
                "font-src": "'self'",
                "object-src": "'none'",
                "connect-src": "'self' http://localhost:3000",
                "frame-ancestors": "'self'"
                        },
            frame_options='SAMEORIGIN',
        )
    else:
        # Minimal production headers (feel free to harden)
        Talisman(app, content_security_policy=None)

    @app.before_request
    def block_hidden_files():
        forbidden = [".git", ".hg", ".bzr", ".darcs", "BitKeeper"]
        if any(f"/{item}" in flask.request.path for item in forbidden):
            return flask.abort(403)

    if is_dev:
        CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}}, supports_credentials=True)
    else:
        CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    
    # Load configuration
    app.config.from_object(config_class)

    # Initialize the MongoDB (this calls init_db(app.config))
    init_db(app.config)

    # Initialize JWT if you're using Flask-JWT-Extended
    jwt = JWTManager(app)

    # Create a Flask-RESTX API instance
    api = Api(
        app,
        version="1.0",
        title="Job Board API",
        description="APIs for Job Board backend"
    )

    # Register your namespaces
    api.add_namespace(job_seekers_ns, path="/api/job_seekers")
    api.add_namespace(companies_ns, path="/api/companies")
    api.add_namespace(job_listings_ns, path="/api/job_listings")
    
    # TODO: Find a way to move those within the api codebase
    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        return identity["email"]

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]      # uses the email address of a user object
        
        # Need a logic to differentiate between if the call to the function
        # is looking for a job_seeker or a company        
        return job_seekers_db.find_job_seeker(identity) or companies_db.find_company(identity)

    return app
