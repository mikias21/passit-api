import os
import math
import json
import random
import bleach
import secrets
import pyaes
import pbkdf2
import binascii
import requests
from Crypto.Cipher import AES
from datetime import datetime
from passlib.context import CryptContext
from Crypto.Random import get_random_bytes
from urllib.parse import urlencode, urlparse
from itsdangerous import URLSafeTimedSerializer

# Local imports
from constants.general import General

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

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

def generate_password_hash(password: str) -> str:
    return password_context.hash(password)

def verify_password_hash(password: str, hash: str) -> bool:
    return password_context.verify(password, hash)

def generate_encoded_url(url: str) -> str:
    parsed_url = urlparse(url)
    encoded_path = parsed_url.path
    encoded_query = urlencode(dict(parsed_url._asdict()))
    encoded_url = parsed_url._replace(path=encoded_path, query=encoded_query).geturl()
    return encoded_url

def generate_clean_input(input: str) -> str:
    sanitized_input = bleach.clean(input, tags=General.ALLOWED_TAGS.value, attributes=General.ALLOWED_ATTRIBUTES.value)
    return sanitized_input

def generate_encrypted_text(input: str, email: str):
    salt = os.urandom(16)
    key = pbkdf2.PBKDF2(email, salt).read(32)
    iv = secrets.randbits(8)
    aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
    cipher_input = aes.encrypt(input)
    return key, iv, cipher_input

def generate_plane_text(key, iv, cyphered_input) -> str:
    aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
    decrypted = aes.decrypt(cyphered_input)
    return decrypted.decode('utf-8')

def generate_user_longitude_latitude(ip: str):
    try:
        response = requests.get(f'https://geolocation-db.com/jsonp/{ip}')
        response = response.content.decode()
        response = response.split("(")[1].strip(")")
        result = json.loads(response)
        return result['latitude'], result['longitude']
    except:
        return 0.0, 0.0