# every __init__.py will treat directories containing files as packages
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config
from flask_limiter import Limiter
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os

# load env variables
load_dotenv()

JWT_SECRET = os.environ.get('JWT_SECRET_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
db = SQLAlchemy()
jwt = JWTManager()
login_manager = LoginManager()


def createapp():
    """
    This function creates the flask app:
    - ensures all security elements of backend are included
    - includes limiting requests and security headers
    - migrates database and starts secure connection to database
    though Config file that has .env variables (so the database url is not hard-coded) 
    - uses flask-cors to make the backend able to communicate
    to the front-end without CORS errors
    - establishes initial 'core' blueprint/directory as root route for 
    dragonflow
    """
    # Flask app creation and enables CORS for Svelte
    app = Flask(__name__)
    CORS(app, resources={r"/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173"], "supports_credentials": True,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }})

    # Uses Config class to establish database connection and inits the database
    app.config.from_object(Config) 

    # establish instance connections
    app.secret_key = SECRET_KEY
    db.init_app(app) 
    jwt.init_app(app)
    login_manager.init_app(app)

    # allows for jwt-extended to automatically verify by token signature
    app.config["JWT_SECRET_KEY"] = JWT_SECRET

    # extended config keys provided by flask; allows for jwt-extended to take advantage of key features.
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["JWT_TOKEN_LOCATION"] = ["headers"] # look for token in headers
    app.config["JWT_HEADER_NAME"] = "Authorization" # look for header in auth
    app.config["JWT_HEADER_TYPE"] = "Bearer" # bearer is the prefix before actual token

    # sends these headers after every request to web-app; extra layer of security
    @app.after_request
    def add_security_headers(response):
       # Add localhost:5173 to the connect-src directive
        response.headers["Content-Security-Policy"] = "default-src 'self'; connect-src 'self' http://localhost:5000 http://localhost:5173; script-src 'self'"
        
        # Add CORS headers explicitly
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        
        return response
    
    # limiter sets a default limit for each page in web-app; prevents bruteforce attacks   
    limiter = Limiter(
         get_remote_address,
         app=app,
         default_limits=["1000 per day"], # one person can only make 1000 requests per day 
        storage_uri="memory://",

        # strategy is just what should happen if limits are exceeded
        strategy="fixed-window"
    )

    # make sure all blueprints have app context
    with app.app_context():
        # IMPORT ALL BLUEPRINTS HERE
        from app.core.routes import core
        from app.auth.routes import auth

        # REGISTER ALL BLUEPRINTS HERE; use core as an example
        app.register_blueprint(core, url_prefix="/")
        app.register_blueprint(auth, url_prefix="/auth")

    from app.models import (
        User, UserPreferences, UserProgram, 
        Courses, UserTermPlanning, RefreshTokens
    )


    # creates migration directory; ignore as its for database development
    migrate = Migrate(app, db)

    # return app as it will be called as a function in run.py
    return app