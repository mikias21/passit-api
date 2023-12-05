import os
import math
import random
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer

def generate_email_activation_token(email: str):
    serializer = URLSafeTimedSerializer(os.getenv('APP_SECRET_KEY'))
    return serializer.dumps(email, salt=os.getenv('APP_SALT'))

def generate_random_otp() -> str:
    digits = [i for i in range(0, 10)]
    otp = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        otp += str(digits[index])
    return otp

def get_date_time_difference(date: str) -> int:
    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
    current_date = datetime.now()
    date_diff = current_date - date
    days_diff = date_diff.days
    return days_diff