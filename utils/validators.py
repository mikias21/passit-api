import os
import ipaddress
from itsdangerous import URLSafeSerializer

def validate_ip(ip: str):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def validate_email_activation_token(token, expiration=3600):
    serializer = URLSafeSerializer(os.getenv('APP_SECRET_KEY'))
    try:
        email = serializer.loads(
            token,
            salf=os.getenv('APP_SALT'),
            max_age=expiration
        )
    except:
        return False
    return email