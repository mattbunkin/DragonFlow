from app import db
from flask_login import UserMixin
from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemySchema

"""
    Users Table 
        - Core authentication and user management system
            • Email, password, user ID, and essential personal information
            • Session tokens and login status tracking
            • Links to preferences and academic progress through foreign keys

    Student Preferences Table
        - Student-specific settings and learning preferences
            • Learning style indicators and academic interests
            • Schedule preferences (time blocks, term preferences)
            • Career goals and industry focus areas

    Program Requirements Table
        - Program-specific academic requirements
            • Complete curriculum mapping for each major
            • Prerequisite chains and course sequences
            • Credit requirements and concentration options
            • Accounts for COOP

    Courses Table
        - Comprehensive course catalog and metadata
            • Course codes, names, credits, and descriptions
            • Term availability and historical offerings
            • Prerequisites and corequisites relationships

    Term Planning Table
        - Schedule management and validation
            • Current and planned course registrations
            • Schedule conflict detection
            • Registration status tracking
            • Accounts for CO-OP

    MAYBE: Resource Links Table
        - Academic support and materials
            • Study resources by course
            • Support service connections
            • Career planning materials
"""

class User(db.Model, UserMixin):
    __tablename__ = "user"
    pid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False)
    drexel_email = db.Column(db.String(60) ,nullable=False)

    # passwords encrypted in any endpoints they're asked for
    hashed_password = db.Column(db.String(80), nullable=False)

    # use db.Date -> (year, month, day) excludes exact time ex. (2023, 1, 1)
    enrollment_date = db.Column(db.Date, nullable=False)
    graduation_date = db.Column(db.Date, nullable=False)

    #if false; must be graduate student and must be manually coded
    undergrad = db.Column(db.Boolean, default=True, nullable=False)
    gpa = db.Column(db.Float, nullable=False)

    # add easy refrencing by establishing relationships to other tables
    user_prefrence = db.relationship("UserPreferences", backref="student_user", lazy=True)
    user_program = db.relationship("UserProgram", backref="student_user", lazy=True)
    user_term_plan = db.relationship("UserTermPlanning", backref="student_user", lazy=True)
    user_refresh_token = db.relationship("RefreshTokens", backref="student_user", lazy=True)

"""
All tables have their foreign key refrence the User primary key:
    This is for: easy usability between tables and to establishing database relationships
    all going back to the student user; all inherit UserMixin for proper auth
"""
# store student preferences for website features
class UserPreferences(db.Model, UserMixin):
    __tablename__ = "user_preferences"  
    id = db.Column(db.Integer, primary_key=True)
    student_pid = db.Columnn(db.Integer, db.ForeignKey(User.pid), nullable=False)

# store major/program type: major requirements, pre-reqs, course code etc.
class UserProgram(db.Model, UserMixin):
    __tablename__ = "user_program"
    id = db.Column(db.Integer, primary_key=True)
    student_pid = db.Columnn(db.Integer, db.ForeignKey(User.pid), nullable=False)


# our own proper course catalogue to refer to after scraping
class Courses(db.Model, UserMixin):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)


# the user's specfic term planning for their next term; must consider CO-OP 
class UserTermPlanning(db.Model, UserMixin):
    __tablename__ = "user_term_planning"
    id = db.Column(db.Integer, primary_key=True)
    student_pid = db.Columnn(db.Integer, db.ForeignKey(User.pid), nullable=False)

# refresh tokens; will use for auth 
class RefreshTokens(db.Model, UserMixin):
    __tablename__ = "refresh_tokens"
    id = db.Column(db.Integer, primary_key=True)
    student_pid = db.Columnn(db.Integer, db.ForeignKey(User.pid), nullable=False)



"""
Use marshmallow's SQLAlchemySchema and validate for
database validation: 
    - prevents SQL injections and is more explicit with preventing
    certain inputs
    - all about data validation and transformation
"""

# Marshmallow input validation Example
class UserSchmea(SQLAlchemySchema):
    class Meta:
        model = User
    pid = fields.Int(dump_only=True) # read-only; can't change

    # Use RegExp to limit user input and length for min/max length
    username = fields.Str(validate=[
        validate.Length(min=3, max=40),
        validate.Regexp("^[a-zA-Z0-9_]+$", 
        error="Username must only contain letters, numbers, underscores")
    ])

    # drexel emails CANNOT be long or too short
    email = fields.Str(validate=[
        validate.Length(min=5, max=30, error="Invalid Drexel Email"),
        validate.Email(error="Not valid email address")
    ])

    # stricter limits because its a password input
    hashed_password = fields.Str(validate=[
        validate.Length(min=10, max=80, error="Password must be minimum of 8 characters"),
        validate.Regexp(
             "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$",
            error="Password must contain at least one letter, one number, and one special character"
        ),
    ])

    # to commit to database must follow this format
    enrollment_date = fields.Date(format="%Y-%m-%d")
    graduation_date = fields.Date(format="%Y-%m-%d")

    # can be changed throughout
    undergrad = fields.Bool()
    gpa = fields.Float()


