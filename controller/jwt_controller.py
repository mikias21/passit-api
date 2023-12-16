import os
from jose import jwt, JWTError
from datetime import timedelta, datetime
from fastapi import HTTPException, status

# Local imports
from constants.auth_error_messages import AuthErrorMessages

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
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AuthErrorMessages.LOGIN_EXPIRED.value)
        return email
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AuthErrorMessages.LOGIN_EXPIRED.value)

def get_current_user(token: str):
    pass