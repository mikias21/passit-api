from fastapi.testclient import TestClient
from main import app

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

client = TestClient(app)

def test_signup_success():
    signup_data = {
        "is_email": "true",
        "is_phone": "false",
        "email": "newuser@example.com",
        "password": "StrongPassword123@",
        "ip_address": "11.11.11.11",
        "user_agent": "Mozilla/5.0 (Windows; U; Windows NT 10.3; x64; en-US) AppleWebKit/535.25 (KHTML, like Gecko) Chrome/53.0.2915.214 Safari/534"
    }
    response = client.post('/signup', json=signup_data)

    assert response.status_code == 201
    assert "Signup successful" in response.text

def test_signup_weak_password():
    signup_data = {
        "is_email": "true",
        "is_phone": "false",
        "email": "newuser@example.com",
        "password": "weakpassword",
        "ip_address": "11.11.11.11",
        "user_agent": "Mozilla/5.0 (Windows; U; Windows NT 10.3; x64; en-US) AppleWebKit/535.25 (KHTML, like Gecko) Chrome/53.0.2915.214 Safari/534"
    }
    response = client.post('/signup', json=signup_data)

    assert response.status_code == 406
    assert "Weak password" in response.text

def test_signup_duplicate_email():
    # Test case where the email is already used for registration
    signup_data = {
        "is_email": "true",
        "is_phone": "false",
        "email": "existinguser@example.com",
        "password": "StrongPassword123@",
        "ip_address": "11.11.11.11",
        "user_agent": "Mozilla/5.0 (Windows; U; Windows NT 10.3; x64; en-US) AppleWebKit/535.25 (KHTML, like Gecko) Chrome/53.0.2915.214 Safari/534"
    }
    response = client.post('/signup', json=signup_data)
   
    assert response.status_code == 406
    assert "Email already taken" in response.text

def test_signup_invalid_user_agent():
    # Test case where the user_agent is missing or invalid
    signup_data = {
        "is_email": "true",
        "is_phone": "false",
        "email": "newuser@example.com",
        "password": "StrongPassword123@",
        "ip_address": "11.11.11.11",
        "user_agent": ""
    }
    response = client.post('/signup', json=signup_data)
   
    assert response.status_code == 406
    assert "Invalid user agent" in response.text

def test_signup_email_sending_error():
    # Test case where there is an issue sending the activation email
    signup_data = {
        "is_email": "true",
        "is_phone": "false",
        "email": "newuser@example.com",
        "password": "StrongPassword123@",
        "ip_address": "11.11.11.11",
        "user_agent": "Mozilla/5.0 (Windows; U; Windows NT 10.3; x64; en-US) AppleWebKit/535.25 (KHTML, like Gecko) Chrome/53.0.2915.214 Safari/534"
    }
    # Mock the email sending function to simulate an error
    # ...

    response = client.post('/signup', json=signup_data)
   
    assert response.status_code == 500
    assert "Error sending activation email" in response.text

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    __package__ = 'api'