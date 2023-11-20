import os
from itsdangerous import URLSafeSerializer

def generate_email_activation_token(email):
    serializer = URLSafeSerializer(os.getenv('APP_SECRET_KEY'))
    return serializer.dumps(email, salt=os.getenv('APP_SALT'))