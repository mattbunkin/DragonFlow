from app import db
from flask_login import UserMixin
from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemySchema
import datetime
# Main Table : crucial user info that is referenced throughout db
class User(db.Model, UserMixin):
    __tablename__ = "users"
    pid = db.Column(db.Integer, primary_key=True)

    def get_id(self):
        return (self.pid)
    
    username = db.Column(db.String(60), nullable=False)
    drexel_email = db.Column(db.String(60) ,nullable=False)

    # passwords encrypted in any endpoints they're asked for
    hashed_password = db.Column(db.String(255), nullable=False)

    # add easy referencing by establishing relationships to other tables
    user_preference = db.relationship("UserPreferences", backref="student_user", lazy=True)
    user_program = db.relationship("UserProgram", backref="student_user", lazy=True)
    user_term_plan = db.relationship("UserTermPlanning", backref="student_user", lazy=True)
    user_refresh_token = db.relationship("RefreshTokens", backref="student_user", lazy=True)



"""
All tables have their foreign key reference the User primary key:
    This is for: easy usability between tables and to establishing database relationships
    all going back to the student user; all inherit UserMixin for proper auth
"""
# store student preferences for website features
class UserPreferences(db.Model, UserMixin):
    __tablename__ = "user_preferences"  
    id = db.Column(db.Integer, primary_key=True)
    student_pid = db.Column(db.Integer, db.ForeignKey(User.pid), nullable=False)

    # can be null if user doesn't want to input any type of data
    user_interests = db.Column(db.String(255), nullable=True)
    user_timing = db.Column(db.String(255), nullable=True)
    user_goals = db.Column(db.String(255), nullable=True)

# store major/program type: major requirements, pre-reqs, course code etc.
class UserProgram(db.Model, UserMixin):
    __tablename__ = "user_program"
    id = db.Column(db.Integer, primary_key=True)
    student_pid = db.Column(db.Integer, db.ForeignKey(User.pid), nullable=False)

    # use db.Date -> (year, month, day) excludes exact time ex. (2023, 1, 1)
    enrollment_date = db.Column(db.Date, nullable=False)
    graduation_date = db.Column(db.Date, nullable=False)

    #if false; must be graduate student and must be manually coded
    is_undergrad = db.Column(db.Boolean, default=True, nullable=False)
    gpa = db.Column(db.Float, nullable=False)

    major = db.Column(db.String(255), nullable=False)
    concentrations = db.Column(db.String(255), nullable=True)
    minor = db.Column(db.String(255), nullable=True)

    credits_min = db.Column(db.Float, nullable=False)
    gpa_min = db.Column(db.Float, nullable=False)
    concentration_needed = db.Column(db.Boolean, nullable=False)
    minor_needed = db.Column(db.Boolean, nullable=False)
    calendar_type = db.Column(db.Boolean, nullable=False)

    # True if CO-OP cycle is 5 year; false if not
    coop_type = db.Column(db.Boolean, nullable=False)


# our own proper course catalogue to refer to after scraping
class Courses(db.Model, UserMixin):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(55), nullable=False)
    course_number = db.Column(db.String(55), nullable=False)
    course_title = db.Column(db.String(1024), nullable=False)
    crn = db.Column(db.Integer, nullable=False, unique=True)
    credits = db.Column(db.String(55), nullable=False)
    instruction_type = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.String(55), nullable=False)
    end_time = db.Column(db.String(55), nullable=False)

     # Add unique constraint
    __table_args__ = (db.UniqueConstraint('crn', 'subject_code', 'course_number'),)
    
class Instructor(db.Model):
    __tablename__ = "instructors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

class CourseInstructor(db.Model):
    __tablename__ = "course_instructors"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('course_id', 'instructor_id'),)

class Day(db.Model):
    __tablename__ = "days"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)

class CourseDay(db.Model):
    __tablename__ = "course_days"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey('days.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('course_id', 'day_id'),)

# the user's specific term planning for their next term; must consider CO-OP 
class UserTermPlanning(db.Model):
    __tablename__ = "user_term_planning"
    id = db.Column(db.Integer, primary_key=True)
    student_pid = db.Column(db.Integer, db.ForeignKey('users.pid'), nullable=False)
    term_id = db.Column(db.Integer, db.ForeignKey('terms.id'), nullable=False)
    
    # Many-to-many relationship with courses through a separate table
    courses = db.relationship('UserTermCourse', backref='term_plan', lazy=True)
    
    # Additional metadata just incase
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    
    __table_args__ = (db.UniqueConstraint('student_pid', 'term_id'),)

class Term(db.Model):
    __tablename__ = "terms"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)  # e.g., "Fall 2023"
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

class UserTermCourse(db.Model):
    __tablename__ = "user_term_courses"
    id = db.Column(db.Integer, primary_key=True)
    term_plan_id = db.Column(db.Integer, db.ForeignKey('user_term_planning.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    
    __table_args__ = (db.UniqueConstraint('term_plan_id', 'course_id'),)

# refresh tokens; will use for auth 
class RefreshTokens(db.Model):
    __tablename__ = "refresh_tokens"
    id = db.Column(db.Integer, primary_key=True)
    
    def get_id(self):
        return (self.pid)

    student_pid = db.Column(db.Integer, db.ForeignKey(User.pid), nullable=False)

    # important token columns; no expiration column since jwt_extended handles this
    token = db.Column(db.String(1024), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False)
    revoked = db.Column(db.Boolean, default=False)



"""
Use marshmallow's SQLAlchemySchema and validate for
database validation: 
    - prevents SQL injections and is more explicit with preventing
    certain inputs
    - all about data validation and transformation
    - all follow same structure at first but have special customizations
    for the specific type of user validation 
"""
# Marshmallow input validation Example
class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
    pid = fields.Int(dump_only=True) # read-only; can't change

    # Use RegExp to limit user input and length for min/max length
    username = fields.Str(validate=[
        validate.Length(min=8, max=40),
        validate.Regexp("^[a-zA-Z0-9_]+$", 
        error="Username must only contain letters, numbers, underscores")
    ])
    
    # drexel emails CANNOT be long or too short
    email = fields.Str(validate=[
        validate.Length(min=5, max=30, error="Invalid Drexel Email"),
        validate.Email(error="Not valid email address")
    ])

    # Drexel password; no need to input validate 
    hashed_password = fields.Str()


class UserPreferencesSchema(SQLAlchemySchema):
    class Meta:
        model = UserPreferences
    # user preferences primary-key and student foreign key fields
    id = fields.Int(dump_only=True)
    student_pid = fields.Int(dump_only=True)

    # interests must have validation because user must user will input it
    user_interests = fields.Str(validate=[
        validate.Length(min=1, max=60, error="Interests can't be too short or too long"),
         validate.Regexp("^[a-zA-Z0-9_]+$", error="Must only be letters or numbers"),
    ])
    
    # timing will be decided by a button: early, afternoon, night/late classes
    user_timing = fields.Str()

    # goals would be based off CCI field also a button: researcher, engineer, etc..
    user_goals = fields.Str()


class UserProgramSchema(SQLAlchemySchema):
    class Meta:
        model = UserProgram
    # user program primary-key and student foreign key fields
    id = fields.Int(dump_only=True)
    student_pid = fields.Int(dump_only=True)

    # to commit to database must follow this format
    enrollment_date = fields.Date(format="%Y-%m-%d")
    graduation_date = fields.Date(format="%Y-%m-%d")

    # can be changed throughout
    is_undergrad = fields.Bool()
    gpa = fields.Float()

    # need this info to even ask about minor/concentration
    major = fields.Str()
    concentrations = fields.Str()
    minor = fields.Str()
    
    credits_min = fields.Float()
    gpa_min = fields.Float()
    
    # for any major; both options must either be true or false
    concentration_needed = fields.Bool()
    minor_needed = fields.Bool()
    coop_type = fields.Bool() # same idea here for CO-OP type

    calendar_type = fields.Bool()


class UserTermPlanningSchema(SQLAlchemySchema):
    class Meta:
        model = UserTermPlanning
    # user term-planning primary-key and student foreign key fields
    id = fields.Int(dump_only=True)
    student_pid = fields.Int(dump_only=True)

    # will add date to be validated soon..
    crn = fields.Int()
    credits = fields.Int()
    course_title = fields.Str()

class RefreshTokenSchema(SQLAlchemySchema):
    class Meta:
        model = RefreshTokens
    # token primary-key and student foreign key fields
    id = fields.Int(dump_only=True)
    student_pid = fields.Int(dump_only=True)
   
    token = fields.Str()
    created_at = fields.DateTime(format="")
    expires_at = fields.DateTime(format="")
    revoked = fields.Bool(dump_only=True)