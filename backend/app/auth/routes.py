from app import db, login_manager
from app.models import User, UserProgram
from app.utils import tokens
from datetime import datetime
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

@login_manager.user_loader
def load_user(pid):
    return User.query.get(int(pid)) #Converts the pid (primary_key) to an integer and fetches the user from the database


# Registration route
@auth.route("/register", methods=["POST"])
def register():
    """
    #### endpoint that receives data from frontend to
    add a new user to database

    ### returns:
    - dict of tokens with ids as the pid from the user schema/table; 
    redirects users to page where they could enter crucial student data
    """
    
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

        # this will be sent to the frontend via dict struct: refer to tokens.py
        user_tokens = tokens.gen_store_tokens(new_user.pid) # crucial as will make token identity same as primary keys
        
        if user_tokens is None:
            return jsonify({"msg": "error generating user tokens"}), 500 # server error

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            user_tokens
        }), 200
    
    except Exception as e:
        db.session.rollback() #the session is rolled back in case of an error.
        logger.error(f"Error creating user: {e}")
        return jsonify({
            "msg": "Could not create user object",
             "error": str(e)
        }), 500


# Login route added token implementation; no GET ever since it's pure API communication
@auth.route("/login", methods=["POST"])
def login():
    """
    ### Logs user in through confirmation of user schema/table 
    redirects to main scheduler page

    ### returns:
    - dict of tokens with ids as the pid from the user schema/table
    """
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
                return jsonify({"msg": "error generating user tokens"}), 500 # server error

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


# last endpoint in auth blueprint; get student's personalized details 
@auth.route("/personalize-account", methods=["POST", "GET"])
@jwt_required() # just want to make sure access token is valid
@login_required
def personalize_account():
    """
    ### endpoint to store crucial student data 
    after they've registered to join dragonflow

    #### Explanation of boolean of data types:
    - dates are in the format "2025-07-15" and
    are of type string

    - user_is_undergrad = True when user is an undergrad, 
    false when grad student

    - user_coop_type = True when it's the 5 year 3 coop program, 
    false when its the 4 year 1 coop program

    - user_calendar_type = True when it's the quarter system, false
    when they are enrolled in the semester system

    ### returns:
    - json of confirmation that student data was stored and redirects
    to main scheduler page
    """
    # try getting personalized form data; could go wrong
    try:
        data = request.get_json()
        
        required_string_fields = ["major", "enrollment_date","graduation_date"]
        required_num_fields = ["gpa", "min_credits", "min_gpa"]

        # if any of the strings in the required fields are empty; add that missing field to list
        missing_fields = [field for field in required_string_fields if not data.get(field)]

        # if any of the required fields have an numerical input thats less than or equal to 0; add that field to list
        invalid_nums = [num_field for num_field in required_num_fields if data.get(num_field) <= 0]

        # if list is not empty it is evaluated to being true
        if missing_fields or invalid_nums:
            return jsonify({
                "msg": "missing fields",
                "fields": missing_fields,
                "number-fields": invalid_nums,
            }), 400
    
        # covert the string from frontend to datetime object format
        try:
            date_format = "%Y-%m-%d"
            user_enrollment_date = datetime.strptime(data.get("enrollment_date"), date_format).date()
            user_graduation_date = datetime.strptime(data.get("graduation_date"), date_format).date()

            if user_enrollment_date >= user_graduation_date:
                return jsonify({
                    "msg": "user's enrollment date can't be after graduation date"
                }), 400

        # raises value error if not found
        except ValueError as e:
            return jsonify({
                "msg": "Invalid date format. Use YYYY-MM-DD"
            }), 400

        # error handling of data before trying to commit to database

    except Exception as e:
        logger.error(f"Error in saving student data route: {e}")
        return jsonify({"msg": "Server error", "error": str(e)}), 500

    # try storing student data into database
    try:
        current_user_id = get_jwt_identity()

        # create a new program for the user
        new_program = UserProgram(
            # string values from form data
            student_pid=current_user_id,
            major=data.get("major"),
            minor=data.get("minor"),
            concentrations=data.get("concentrations"),
            enrollment_date=user_enrollment_date,
            graduation_date=user_graduation_date,

            # boolean values from form data
            minor_needed=data.get("minor_needed"),
            concentration_needed=data.get("concentration_needed"),
            is_undergrad=data.get("undergrad"),
            coop_type=data.get("coop_type"),
            calendar_type=data.get("calendar_type"),

            # numerical values from form data
            gpa=float(data.get("gpa")),
            gpa_min=float(data.get("min_gpa")),
            credits_min=float(data.get("min_credits"))
        )

        # commit user program to db and return 200 successful HTTP code
        db.session.add(new_program)
        db.session.commit()

        return jsonify({
            "msg": "Successfully added user program"
        }), 200 
    
    # stop any operations on db and return logged error
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error storing user data: {e}")

        return jsonify({
            "msg": "Could not save student data to db", 
            "error": str(e)
        }), 500