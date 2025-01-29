# every __init__.py will treat directories containing files as packages
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os

# load env variables
load_dotenv()

JWT_SECRET = os.environ.get('JWT_SECRET_KEY')
db = SQLAlchemy()

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
    CORS(app) 
    # Uses Config class to establish database connection and inits the database
    app.config.from_object(Config) 
    db.init_app(app) 

    # sends these headers after every request to web-app; extra layer of security
    @app.after_request
    def add_security_headers(response):
         response.headers["Content-Security-Policy"] = """
            default-src 'self';
            connect-src 'self' http://localhost:5000; 
            script-src 'self';
        """

    # limiter sets a default limit for each page in web-app; prevents bruteforce attacks   
    limiter = Limiter(
         get_remote_address,
         app=app,
         default_limits=["1000 per day"], # one person can only make 1000 requests per day 
        storage_uri="memory://",

        # strategy is just what should happen if limits are exceeded
        strategy="fixed-window"
    )

    # IMPORT ALL BLUEPRINTS HERE
    from app.core.routes import core



    # REGISTR ALL BLUEPRINTS HERE; use core as an example
    app.register_blueprint(core, url_prefix="/")



    # creates migration directory; ignore as its for database development
    migrate = Migrate(app, db)

    # return app as it will be called as a function in run.py
    return app