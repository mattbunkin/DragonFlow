from app import db
from flask_login import UserMixin
from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemySchema

# Main Table : crucial user info that is referenced throughout db
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
    user_goals = db.Column(db.String(255, nullable=True))

# store major/program type: major requirements, pre-reqs, course code etc.
class UserProgram(db.Model, UserMixin):
    __tablename__ = "user_program"
    id = db.Column(db.Integer, primary_key=True)
    student_pid = db.Column(db.Integer, db.ForeignKey(User.pid), nullable=False)

    user_major = db.Column(db.String(255), nullable=False)
    user_credit_min = db.Column(db.Float, nullable=False)
    user_gpa_min = db.Column(db.Float, nullable=False)
    user_concentration_needed = db.Column(db.Boolean, nullable=False)
    user_minor_needed = db.Column(db.Boolean, nullable=False)
    user_calendar_type = db.Column(db.String(255), nullable=False)

    # True if CO-OP cycle is 5 year; false if not
    user_coop_type = db.Column(db.Boolean, nullable=False)


# our own proper course catalogue to refer to after scraping
class Courses(db.Model, UserMixin):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    # empty because were waiting for scraped data


# the user's specific term planning for their next term; must consider CO-OP 
class UserTermPlanning(db.Model, UserMixin):
    __tablename__ = "user_term_planning"
    id = db.Column(db.Integer, primary_key=True)
    student_pid = db.Column(db.Integer, db.ForeignKey(User.pid), nullable=False)
    # empty as we wait for scraped data

# refresh tokens; will use for auth 
class RefreshTokens(db.Model, UserMixin):
    __tablename__ = "refresh_tokens"
    id = db.Column(db.Integer, primary_key=True)
    student_pid = db.Column(db.Integer, db.ForeignKey(User.pid), nullable=False)

    # important token columns; authorize user
    token = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
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
        validate.Length(min=3, max=40),
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

    # to commit to database must follow this format
    enrollment_date = fields.Date(format="%Y-%m-%d")
    graduation_date = fields.Date(format="%Y-%m-%d")

    # can be changed throughout
    undergrad = fields.Bool()
    gpa = fields.Float()


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

    # need this info to even ask about minor/concentration
    user_major = fields.Str()
    user_credit_min = fields.Float()
    user_gpa_min = fields.Float()
    
    # for any major; both options must either be true or false
    user_concentration_needed = fields.Bool()
    user_minor_needed = fields.Bool()
    user_coop_type = fields.Bool() # same idea here for CO-OP type

    user_calendar_type = fields.Str()


class UserTermPlanningSchema(SQLAlchemySchema):
    class Meta:
        model = UserTermPlanning
    # user term-planning primary-key and student foreign key fields
    id = fields.Int(dump_only=True)
    student_pid = fields.Int(dump_only=True)

    # leave empty as we plan out courses table


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