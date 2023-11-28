import os
from itsdangerous import URLSafeTimedSerializer

def generate_email_activation_token(email):
    serializer = URLSafeTimedSerializer(os.getenv('APP_SECRET_KEY'))
    return serializer.dumps(email, salt=os.getenv('APP_SALT'))