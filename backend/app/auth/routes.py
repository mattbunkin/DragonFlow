from app import db
from app.models import User  
from utils import tokens
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
        username = request.form.get("username")
        password = request.form.get("password")
        drexel_email = request.form.get("drexel_email")

        # need both these values in format: YYYY-MM-DD, will format in frontend
        enrollment_date = date(request.form.get("enrollment_date"))
        graduation_date = date(request.form.get("graduation_date"))

        # when making html checkbox: name='student_type',  value='undergrad'
        undergrad = request.form.get("student_type")
        gpa = float(request.form.get("gpa"))

    except Exception as e:
        flash(f"Please input correct info: {str(e)}")
        return jsonify({"msg": "invalid input form"}), 401

    user = User.query.filter_by(username=username).first()

    if user != None:
        flash("User/Username already exists")

    else:
        try:
            # create a new user object in database
            new_user = User(
                username=username,
                drexel_email=drexel_email,
                hashed_password=generate_password_hash(password),  
                enrollment_date=enrollment_date,
                graduation_date=graduation_date,
                undergrad=undergrad,
                gpa=gpa
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please login.", "success")
            return jsonify({"msg": "successful registration"}), 200
        
        except Exception as e:
            flash(f"Potential server error: {str(e)}")
            return jsonify({"msg": "could not create user object"}), 500


# Login route added token implementation; no GET ever since it's pure API communication
@auth.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    # will return the User object if found; if not the type is 'None'
    if user != None:
        flash("User/Username already exists")

    if user and check_password_hash(user.hashed_password, password):
        login_user(user)
        flash("Logged in successfully!", "success")
        
        # this will be sent to the frontend via dict struct: refer to tokens.py
        user_tokens = tokens.gen_store_tokens(user.pid) # crucial as will make token identity same as primary keys

        if user_tokens is None:
            return jsonify({"msg": "error generating tokens"}), 500 # server error

        return jsonify(
            user_tokens
        ), 200
    else:
        flash("Invalid username or password", "error")
        return jsonify({"msg": "invalid credentials"}), 401


# complete example of using jwt tokens for routing authentication
@auth.route("/logout")
@jwt_required(refresh=True) # MUST have refresh not access token
@login_required
def logout():
    # code will only run if refresh token valid
    current_user_id = get_jwt_identity() # gets user id from refresh token
    
    # will logout user no matter what
    logout_user()
    flash("Logged out successfully!", "success")

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
        flash(f"Unexpected error in logout route: {str(e)}")
        return jsonify({"msg": "Server error during logout"}), 500


# Dashboard route (protected)
@auth.route("/dashboard")
@jwt_required() # just want to make sure access token is valid
@login_required
def dashboard():
    return f"Welcome to the dashboard, {current_user.username}!"

