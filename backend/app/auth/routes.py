from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash  
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app import db
from app.models import User  
from utils import tokens
from flask_jwt_extended import (
    jwt_required, 
    get_jwt,
    get_jwt_header,
    get_jti,
    get_jwt_identity
)

auth = Blueprint("auth", __name__)

# Flask-Login setup
login_manager = LoginManager()

@login_manager.user_loader
def load_user(pid):
    return User.query.get(int(pid)) #Converts the pid (primary_key) to an integer and fetches the user from the database


# Login route
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.hashed_password, password):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("auth.dashboard"))
        else:
            flash("Invalid username or password", "error")


# Dashboard route (protected)
@auth.route("/dashboard")
@jwt_required() # just want to make sure access token is valid
@login_required
def dashboard():
    return f"Welcome to the dashboard, {current_user.username}!"


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
        print(f"Unexpected error in logout route: {str(e)}")
        return jsonify({"msg": "Server error during logout"}), 500



# Registration route
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        drexel_email = request.form.get("drexel_email")
        enrollment_date = request.form.get("enrollment_date")
        graduation_date = request.form.get("graduation_date")
        undergrad = request.form.get("undergrad") == "true"
        gpa = float(request.form.get("gpa"))

        user = User.query.filter_by(username=username).first()

        if user:
            flash("Username already exists", "error")
        else:
            #create a new user object in database
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
            return redirect(url_for("auth.login"))

