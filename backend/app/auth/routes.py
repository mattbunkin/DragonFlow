import os 
import json
import subprocess
from dotenv import load_dotenv
from scripts import model
from scripts import prereqs
from app import db, login_manager
from app.models import * 
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
    get_jwt_identity,
    create_access_token # get user_id from token (same as primary key for user from db)
)
import logging #will give us better errors printed in the console

# load in course data 
load_dotenv()
COURSE_DATA = os.environ.get("DATA_FILE")
RMP_PATH = os.environ.get("RMP_PATH")

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# create blueprint
auth = Blueprint("auth", __name__)

#open open the course data file and load it into a variable
with open(COURSE_DATA) as f:
    course_data = json.load(f)
    
@login_manager.user_loader
def load_user(pid):
    return User.query.get(int(pid)) #Converts the pid (primary_key) to an integer and fetches the user from the database

# Registration/sign up route
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
            return (
                jsonify({"msg": "Passwords do not match"}),
                400,
            )  # User-friendly message for client (display to frontend)

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

        # this will be sent to the frontend via dict struct: refer to tokens.py
        user_tokens = tokens.gen_store_tokens(
            new_user.pid
        )  # crucial as will make token identity same as primary keys

        if user_tokens is None:
            db.session.rollback()
            return jsonify({"msg": "error generating user tokens"}), 500  # server error

        return jsonify(user_tokens), 200
    
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


@auth.route("/refresh-token", methods=["GET", "POST"])
@jwt_required(refresh=True)
def refresh_token():
    """
    ### Endpoint to refresh access token using valid refresh token
    returns new access token with proper status code
    """
    current_user_id = get_jwt_identity()

    # generate new access token
    user_access_token = create_access_token(current_user_id)

    return jsonify({"access_token": user_access_token}), 200

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
    
# proxy flask get my professor api -- documentation soon.
@auth.route('/professor-rating', methods=['GET', 'OPTIONS'])
def get_professor_rating():
     # Handle preflight requests for CORS
    if request.method == 'OPTIONS':
        response = jsonify({"message": "preflight"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
        return response
        
    professor_name = request.args.get('name')
    
    if not professor_name:
        return jsonify({"error": "Professor name is required"}), 400
    
    try:
        # Use the new script path
        script_path = RMP_PATH
        cmd = ["node", script_path, professor_name]
        
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({"error": "Failed to fetch professor data", "details": result.stderr}), 500
            
        try:
            data = json.loads(result.stdout)
            return jsonify(data)
        
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return jsonify({"error": "Invalid response from RMP API", "output": result.stdout}), 500
    
    except Exception as e:
        logger.error(f"Exception in professor-rating: {e}")
        return jsonify({"error": str(e)}), 500


# basic endpoint no authentication quite yet   
@auth.route("/course-retriever", methods=["GET", "POST"])
def course_retriever():
    """
    ### Endpoint that gets data to check if course exists
    endpoint will receive data when user types in the searchbar a 
    course with its course subject code and number; it returns ALL
    instances of course if found and the probability of success
    for course by feeding the model the course CRN and student's gpa. Returns and displays error
    if not found.
    """
    # get data from user search
    data = request.get_json()

    gpa = data.get("gpa")
    course = data.get("course")

    try:
        # get one course's entire CRN for the quarter 
        course_crns = prereqs.get_course_crn(course_name=course, find_all=True) 
        course_info = prereqs.get_crns_info(course_crns)
        
        # get model to calculate probability 
        try:
            gpa = float(gpa)
            course_crn = str(course_crns[0])
            probability = model.predict_success_probability(gpa, course_crn)
            # return list of dicts back to frontend
            return jsonify({
                "course_data": course_info,
                "probability_score": int(probability * 100)
            }), 200

        # error if type or crn is not found
        except ValueError as e:
            return jsonify({
                "msg": "enter valid crn or gpa types",
                "error": str(e),
            }), 400

    # return error shown from scripts if not able to look up any of these
    except LookupError as e:
        return jsonify({
            "msg": "Could not find course in course data.",
            "error": str(e)
        }), 400



@auth.route("/get-interests", methods=["GET", "POST"])
def get_interests():
    """
    API endpoint to filter courses based on user preferences.
    Accepts JSON input with filtering criteria and returns matching course CRNs.
    """
    
    # ====================== REQUEST VALIDATION ======================
    # Check if the request contains JSON data
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400  # 400 = Bad Request

    # Parse the JSON data from the request
    data = request.get_json()
    
    # Check if any data was provided
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Get filter parameters with None as default if not provided
    class_time = data.get("class_time")         # Expected: "Morning", "Afternoon", "Evening"
    class_size = data.get("class_size")        # Expected: "Small", "Large"
    class_difficulty = data.get("class_difficulty")  # Placeholder for future use (RMP)
    instruction_type = data.get("instruction_type")  # Expected: "Online", "In Person"
    preferred_course = data.get("preferred_course")  # Expected format: "CS172" or "UNIVCI101"

    subject_match = course_number_match = None
    
    if preferred_course:
        preferred_course = preferred_course.strip().upper()
        
        for i, char in enumerate(preferred_course):
            if char.isdigit():
                subject_match = preferred_course[:i]
                course_number_match = preferred_course[i:]
                break
            
    matching_crns = []

    # ====================== COURSE FILTERING LOGIC ======================
    # Iterate through all courses in course_data (key=CRN, value=course details)
    for crn, course in course_data.items():
        match = True  # Start by assuming the course matches all criteria

        # --------------------- COURSE CODE FILTER ---------------------
        if preferred_course:
            
            subject = course.get("subject_code", "").upper()
            number = course.get("course_number", "").upper()
            
            if subject != subject_match or number != course_number_match:
                match = False

        # --------------------- CLASS TIME FILTER ---------------------
        if class_time:  # Only apply filter if class_time was specified
            start_time = course.get('start_time')
            
            # If course has no start time, exclude it
            if not start_time:
                match = False
            else:
                try:
                    # Extract the hour from start time (format "HH:MM")
                    start_hour = int(start_time.split(":")[0])
                    
                    # Check against time categories
                    if class_time == "Morning" and not (8 <= start_hour < 12):
                        match = False
                    elif class_time == "Afternoon" and not (12 <= start_hour < 16):
                        match = False
                    elif class_time == "Evening" and not (16 <= start_hour <= 22):
                        match = False
                except (ValueError, AttributeError):
                    match = False # Handle invalid time format or missing data
        
        # --------------------- CLASS SIZE FILTER ---------------------
        # Only check size if previous filters haven't disqualified the course
        if match and class_size:
            size = course.get('max_enroll')
            
            if not size:  # No enrollment data available
                match = False
            else:
                try:
                    size = int(size)  # Convert to integer
                    
                    # Apply size thresholds
                    if class_size == "Large" and size <= 50:
                        match = False  # Not large enough
                    elif class_size == "Small" and size > 50:
                        match = False  # Too large
                except ValueError:
                    # Handle invalid size data
                    match = False
        
        # --------------------- INSTRUCTION TYPE FILTER ---------------------
        if match and instruction_type:
            # Normalize strings for case-insensitive comparison
            instruction_method = course.get('instruction_method', '').lower()
            requested_type = instruction_type.lower()
            
            # Check instruction method matches request
            if requested_type == "online" and instruction_method != "online-asynchronous":
                match = False
            elif requested_type == "in person" and instruction_method != "face to face":
                match = False
        
        # --------------------- CLASS DIFFICULTY (PLACEHOLDER) ---------------------
        if match and class_difficulty:
            # Future implementation point for difficulty filtering
            pass  # Currently does nothing

        # If all active filters were passed, add to results
        if match:
            matching_crns.append(crn)  # Store the matching course's CRN
            
    # Return matching CRNs as JSON response
    return jsonify({
        "matching_courses": matching_crns,
        "count": len(matching_crns) #include count of course matches (maybe useful for frontend)
    })

@auth.route("/schedule-saver", methods=["GET", "POST"])
@jwt_required()
def schedule_saver():
    """
    ### end point to allow the schedule the user has made in scheduler page to be saved in DB
    """
    # receive data from svelte
    current_user_id = get_jwt_identity()
    data = request.get_json()
    schedule = data.get("schedule")
    term_id = data.get("term_id")  # Assuming user selects a term

    if not schedule or not term_id:
        return jsonify({"error": "Missing required data"}), 400
    
    # Get or create user term plan
    term_plan = UserTermPlanning.query.filter_by(
        student_pid=current_user_id,
        term_id=term_id
    ).first()
    
    if not term_plan:
        term_plan = UserTermPlanning(student_pid=current_user_id, term_id=term_id)
        db.session.add(term_plan)
        db.session.flush()
    
    # Process each course
    for course_data in schedule:
        # Get or create the course
        course = Courses.query.filter_by(crn=course_data.get("crn")).first()
        
        if not course:
            course = Courses(
                subject_code=course_data.get("subject_code"),
                course_number=course_data.get("course_number"),
                course_title=course_data.get("course_title"),
                crn=course_data.get("crn"),
                credits=course_data.get("credits"),
                instruction_type=course_data.get("instruction_type"),
                start_time=course_data.get("start_time"),
                end_time=course_data.get("end_time")
            )
            db.session.add(course)
            db.session.flush()
            
            # Add instructors
            for instructor_data in course_data.get("instructors", []):
                instructor = Instructor.query.filter_by(name=instructor_data.get("name")).first()
                if not instructor:
                    instructor = Instructor(name=instructor_data.get("name"))
                    db.session.add(instructor)
                    db.session.flush()
                
                course_instructor = CourseInstructor(
                    course_id=course.id,
                    instructor_id=instructor.id
                )
                db.session.add(course_instructor)
            
            # Add days
            for day_data in course_data.get("days", []):
                day = Day.query.filter_by(name=day_data.get("day")).first()
                if not day:
                    day = Day(name=day_data.get("day"))
                    db.session.add(day)
                    db.session.flush()
                
                course_day = CourseDay(
                    course_id=course.id,
                    day_id=day.id
                )
                db.session.add(course_day)
        
        # Add course to user's term plan
        user_term_course = UserTermCourse.query.filter_by(
            term_plan_id=term_plan.id,
            course_id=course.id
        ).first()
        
        if not user_term_course:
            user_term_course = UserTermCourse(
                term_plan_id=term_plan.id,
                course_id=course.id
            )
            db.session.add(user_term_course)
    
    try:
        db.session.commit()
        return jsonify({"msg": "Successfully saved schedule"}), 200
    
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500