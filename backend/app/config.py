# will be the configuration for the database models were using
import os
from dotenv import load_dotenv
load_dotenv() # load env variables


# establishes connection to the dragonflow postgreSQL database
DATABASE_URL = os.environ.get('DATABASE_URL')
class Config:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
