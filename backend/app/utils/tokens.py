from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)
import logging
from datetime import datetime, timedelta
from app.models import RefreshTokens
from app import db

"""
When working within the routes.py files the routes need a way of knowing whether 
some operation on a token is successful; this is why we return boolean types
for all functions in tokens.py, it allows us to use if/elif statements
when checking if functions ran successfully.

    True: Querying and specific token function worked perfectly
    False: Querying worked, but token could be expired, invalid or flawed.
    None: Only for generating tokens function; None tells us we couldn't generate tokens.
"""

# config logger for refresh token debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# remember generating tokens from jwt-extended returns dictionaries
def store_refresh_token(user_id: int, token: dict) -> bool:
    # delete any token before storing new one
    try:
        RefreshTokens.query.filter_by(student_pid=user_id).delete()
        db.session.commit()
    except:
        pass

    new_token = RefreshTokens(
        student_pid = user_id,
        token = token,
        created_at = datetime.now(),
        revoked=False
    )
    
    try:
        db.session.add(new_token)
        db.session.commit()
        return True # complete
    
    except Exception as e:
        logger.error(f"error storing refresh token: {e}")
        db.session.rollback() # if failed, stop session
        return False  # return False failed operation


# generates tokens and returns them inside a dictionary to be accessed through keys
def gen_store_tokens(user_id: int) -> dict | None:
    user_refresh_token = create_refresh_token(user_id)
    user_access_token = create_access_token(user_id)

    # if operation was completed (storing function returns True)
    if store_refresh_token(user_id, user_refresh_token):

        # return a dictionary with the user's encoded refresh & access
        return {
            "user_refresh_token": user_refresh_token,
            "user_access_token": user_access_token 
        }
    # if storing function fails (return False); else return None to indicate the token wasn't created 
    else:
        logger.error("Error storing refresh tokens: db session cancelled")
        db.session.rollback()
        return None


# tries to find token; makes it unaccessible/revoked if found
def revoke_refresh_token(user_id) -> bool:
    try: 
        # if user wants to logout 
        token = RefreshTokens.query.filter_by(
            student_pid=user_id,
            revoked=False,
        ).first()

        token.revoked = True
        db.session.commit()

        # if token has been revoked
        return True

    except Exception as e:
        db.session.rollback()
        return False


# tells us whether the token is valid; uses exceptions to tell us about token's validity in database 
def check_refresh_token(user_id: int) -> bool:
    # get current token identity / user_id with method
    try:
        token = RefreshTokens.query.filter_by(
            student_pid=user_id,
            revoked=False, # getting non-revoked tokens
        ).first()

        # was token found? if not; return False
        if not token:
            return False
        
        # if token is indeed valid
        return True

    # if we couldn't even query the token 
    except Exception as e:
        db.session.rollback()
        return False

# can use this function to clear the cache of tokens; True if operation complete
def clear_refresh_token(user_id: int) -> bool:
    try:
        token = RefreshTokens.query.filter_by(
            student_pid=user_id,
            revoked=True
        ).delete()
        db.session.commit()
        return True

    # return error if couldn't find token or error occurred 
    except Exception as e:
        db.session.rollback()
        return False