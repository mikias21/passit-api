from fastapi import Response, status
from email_validator import validate_email, EmailNotValidError

# Local imports
from controller.email_controller import send_email
from schemas.forgot_password import ForgotPassword
from database.database_connection import users_collection
from constants.auth_error_messages import AuthErrorMessages
from utils.generators import generate_email_activation_token
from utils.email_template_generator import generate_forgot_password_template

async def forgot_password_controller(email: ForgotPassword):
    try:
        email_info = validate_email(email.email)
        email.email = email_info.normalized
        
        user = users_collection.find_one({'user_email': email.email})
        if user:
            token = generate_email_activation_token(email.email)
            email_msg = generate_forgot_password_template(token)
            if send_email("Forgot Password", email.email, email_msg) == 200:
                return Response(AuthErrorMessages.FORGOT_PASSWORD.value, status.HTTP_200_OK)
        else:
            return Response(AuthErrorMessages.USER_NOT_FOUND.value, status.HTTP_404_NOT_FOUND)
    except EmailNotValidError:
        return Response(AuthErrorMessages.INVALID_EMAIL.value, status.HTTP_406_NOT_ACCEPTABLE)