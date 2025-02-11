from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)
from datetime import datetime, timedelta
from app.models import RefreshTokens
from app import db

"""
When working within the routes.py files the return types specify
    True/False: tells us the querying/operations worked
    but token was flawed (invalid, expired etc). 

    Exceptions/e: tells us we couldn't even query without an error.
"""

# remember generating tokens from jwt-extended returns dictionaries
def store_refresh_token(user_id: int, token: dict) -> bool:
    # delete any token before storting new one
    RefreshTokens.query.filter_by(user_id=user_id).delete()

    new_token = RefreshTokens(
        user_id = user_id,
        token = token,
        created_at = datetime.now(),
    )

    try:
        db.session.add(new_token)
        db.session.commit()
        return True # complete
    
    except Exception as e:
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
        db.session.rollback()
        return None


# tries to find token; makes it unaccessible/revoked if found
def revoke_refresh_token(user_id) -> True | Exception:
    try: 
        # if user wants to logout 
        token = RefreshTokens.query.filter_by(
            user_id=user_id,
            revoked=False,
        ).first()

        token.revoked = True
        db.session.commit()

        # if token has been revoked
        return True

    except Exception as e:
        db.session.rollback()
        return e


# tells us whether the token is valid; uses exceptions to tell us about token's validity in database 
def check_refresh_token(user_id: int) -> bool | Exception:
    # get current token identity / user_id with method
    try:
        token = RefreshTokens.query.filter_by(
            user_id=user_id,
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
        return e

# can use this function to clear the cache of tokens; True if operation complete
def clear_refresh_token(user_id: int) -> True | Exception:
    try:
        token = RefreshTokens.query.filter_by(
            user_id=user_id,
            revoked=True
        ).delete()
        db.session.commit()
        return True

    # return error if couldn't find token or error occurred 
    except Exception as e:
        db.session.rollback()
        return e