import os
from jose import jwt, JWTError
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

# Local imports

def create_access_token(data: dict):
    to_encode = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=int(os.getenv('ACCOUNT_LOGIN_TOKEN_EXPIRATION_MINS')))
    to_encode.update({'expire': expire_time.strftime("%Y-%m-%d %H:%M:%S")})
    encoded_jwt = jwt.encode(to_encode, os.getenv("ACCOUNT_LOGIN_TOKEN_SECRET_KEY"), os.getenv("JWT_ALGORITHM"))
    return encoded_jwt

def verify_access_token(token: str, cred_exception):
    try:
        payload = jwt.decode(token, os.getenv("ACCOUNT_LOGIN_TOKEN_SECRET_KEY"), os.getenv("JWT_ALGORITHM"))
        email: str = payload['user_email']
        if email is None:
            raise cred_exception
        return email
    except JWTError as e:
        raise cred_exception

def get_current_user(token: str):
    pass