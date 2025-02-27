from app import db
from app.models import User  
from app.utils import tokens
from datetime import date 
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash  
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_jwt_extended import (
    jwt_required, # decorator
    get_jwt, # full payload
    get_jwt_header, # header data
    get_jti, # very unique token identifier 
    get_jwt_identity # get user_id from token (same as primary key for user from db)
)
import logging #will give us better errors printed in the console

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# create blueprint
auth = Blueprint("auth", __name__)

# Flask-Login setup
login_manager = LoginManager()

@login_manager.user_loader
def load_user(pid):
    return User.query.get(int(pid)) #Converts the pid (primary_key) to an integer and fetches the user from the database


# Registration route
@auth.route("/register", methods=["POST"])
def register():
    # try getting the form data; could go wrong
    try:
        data = request.get_json()
        
        username = data.get("username")
        password = data.get("password")
        drexel_email = data.get("email")
        confirm_password = data.get("confirm_password")


        if not username or not password or not drexel_email or not confirm_password:
            return jsonify({"msg": "Missing required fields"}), 400
        
        
        # Check if passwords match
        if password != confirm_password:
            logger.error("Passwords don't match")  # Log error for devs
            return jsonify({"msg": "Passwords do not match"}), 400  # User-friendly message for client (display to frontend)

        
        
    except Exception as e:
        logger.error(f"Error in register route: {e}")
        return jsonify({"msg": "Invalid input form", "error": str(e)}), 400

    try:
        # create a new user object in database
        new_user = User(
            username=username,
            drexel_email=drexel_email,
            hashed_password=generate_password_hash(password),  
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "Successful registration"}), 200
    
    except Exception as e:
        db.session.rollback() #the session is rolled back in case of an error.
        logger.error(f"Error creating user: {e}")
        return jsonify({"msg": "Could not create user object", "error": str(e)}), 500


# Login route added token implementation; no GET ever since it's pure API communication
@auth.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not password:
            return jsonify({"msg": "Missing username or password"}), 400

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.hashed_password, password):
            login_user(user)
            
            # this will be sent to the frontend via dict struct: refer to tokens.py
            user_tokens = tokens.gen_store_tokens(user.pid) # crucial as will make token identity same as primary keys

            if user_tokens is None:
                return jsonify({"msg": "Error generating tokens"}), 500 # server error

            return jsonify(user_tokens), 200
        else:
            return jsonify({"msg": "Invalid credentials"}), 401

    except Exception as e:
        logger.error(f"Error in login route: {e}")
        return jsonify({"msg": "Server error during login", "error": str(e)}), 500


# complete example of using jwt tokens for routing authentication
@auth.route("/logout")
@jwt_required(refresh=True) # MUST have refresh not access token
@login_required
def logout():
    
    # code will only run if refresh token valid
    current_user_id = get_jwt_identity() # gets user id from refresh token
    
    # will logout user no matter what
    logout_user()

    # try to perform any of the functions
    try:
        # tells us function worked; user's refresh tokens were removed
        if tokens.revoke_refresh_token(user_id=current_user_id):
            return jsonify({"msg": "Successfully removed token"}), 200
        
        # some error in removing; token didn't exist or maybe something else..
        else:
            return jsonify({"msg": "Failed to revoke refresh token"}), 401
        
    # bigger error; could mean querying didn't work etc.
    except Exception as e:
        logger.error(f"Error in logout route: {e}")
        return jsonify({"msg": "Server error during logout", "error": str(e)}), 500


# Dashboard route (protected)
@auth.route("/dashboard")
@jwt_required() # just want to make sure access token is valid
@login_required
def dashboard():
    try:
        return f"Welcome to the dashboard, {current_user.username}!"
    except Exception as e:
        logger.error(f"Error in dashboard route: {e}")
        return jsonify({"msg": "Server error", "error": str(e)}), 500