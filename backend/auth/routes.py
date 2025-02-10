from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import check_password_hash, generate_password_hash  
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app import models,User, db  

auth = Blueprint("auth", __name__)

# Flask-Login setup
login_manager = LoginManager()

@login_manager.user_loader
def load_user(pid):
    return User.query.get(int(pid)) #Converts the pid (primarykey) to an integer and fetches the user from the database

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

#we will need to create this page at a later date
    return render_template("login.html")

# Dashboard route (protected)
@auth.route("/dashboard")
@login_required
def dashboard():
    return f"Welcome to the dashboard, {current_user.username}!"

# Logout route
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for("auth.login"))

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

#we will need to make this page
    return render_template("register.html")