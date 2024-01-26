import os
from jose import jwt, JWTError
from datetime import timedelta, datetime

# Local imports
from database.database_connection import users_login_token_collection

def create_access_token(data: dict):
    to_encode = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=int(os.getenv('ACCOUNT_LOGIN_TOKEN_EXPIRATION_MINS')))
    to_encode = {
        "exp": expire_time,
        **data
    }
    encoded_jwt = jwt.encode(to_encode, os.getenv("ACCOUNT_LOGIN_TOKEN_SECRET_KEY"), os.getenv("JWT_ALGORITHM"))
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, os.getenv("ACCOUNT_LOGIN_TOKEN_SECRET_KEY"), os.getenv("JWT_ALGORITHM"))
        email: str = payload['user_email']
        if email is None:
            return False
        
        # Check token in DB
        tokens = users_login_token_collection.find({"email": email})
        for token_dict in tokens:
            if token_dict['token'] == token:
                return False
        return email
    except JWTError as e:
        return False

def get_current_user(token: str):
    pass