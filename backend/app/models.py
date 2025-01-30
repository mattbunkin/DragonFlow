from app import db
from flask_login import UserMixin
from marshmallow import Schema, validate
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

# store sensitive student user info
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


# store student preferences for website features
class UserPreferences(db.Model, UserMixin):
    __tablename__ = "user_preferences"  
    pass

# store major/program type: major requirements, pre-reqs, course code etc.
class UserProgram(db.Model, UserMixin):
    __tablename__ = "user_program"
    pass

# our own proper course catalogue to refer to after scraping
class Courses(db.Model, UserMixin):
    __tablename__ = "courses"
    pass

# the user's specfic term planning for their next term
class UserTermPlanning(db.Model, UserMixin):
    __tablename__ = "user_term_planning"
    pass

# refresh tokens; will use for auth 
class RefreshTokens(db.Model, UserMixin):
    __tablename__ = "refresh_tokens"
    pass