import os
import ipaddress
from urllib.parse import urlparse
from itsdangerous import URLSafeTimedSerializer

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
            max_age=int(os.getenv('ACCOUNT_ACTIVATION_TOKEN_EXPIRATION_SECONDS'))
        )
    except Exception:
        return False
    return email

def validate_url(url: str) -> bool:
    parsed_url = urlparse(url)

    if parsed_url.scheme and parsed_url.netloc:
        return True
    return False