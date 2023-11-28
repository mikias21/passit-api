import os
import ipaddress
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

def validate_ip(ip: str):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def validate_email_activation_token(token):
    serializer = URLSafeTimedSerializer(os.getenv('APP_SECRET_KEY'))
    try:
        email = serializer.loads(
            token,
            salt=os.getenv('APP_SALT'),
            max_age=int(os.getenv('ACCOUNT_ACTIVATION_TOKEN_EXPIRATION_SECCONDS'))
        )
    except SignatureExpired as e:
        return False
    return email