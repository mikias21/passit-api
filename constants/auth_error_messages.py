from enum import Enum

class AuthErrorMessages(Enum):
    NO_SIGNUP_METHOD = "Choose signup method, email or phone."
    INVALID_EMAIL = "Invalid email, Please use valid email to signup."
    INVALID_PASSWORD = "Password should be 8 - 16 characters, lower case, uppercase, digits and symbols."
    INVALID_IP = "Seems like your IP is invalid, Check your network settings."
    INVALID_USERAGENT = "Invalid User Agent, Check device or browser."
    SIGNUP_SUCCESS = "Account created, please check email for verification."
    EMAIL_TAKEN = "Email already taken, use a different email."
    EMAIL_SENDING_ERROR = "Unable to send email, please try again later."