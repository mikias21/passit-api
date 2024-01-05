from fastapi import Response, status, HTTPException
from email_validator import validate_email, EmailNotValidError

# Local imports
from controller.email_controller import send_email
from database.database_connection import users_collection
from constants.auth_error_messages import AuthErrorMessages
from utils.generators import generate_email_activation_token
from utils.email_template_generator import generate_forgot_password_template
from schemas.forgot_password import ForgotPassword, ForgotPasswordResponseModel

async def forgot_password_controller(email: ForgotPassword) -> ForgotPasswordResponseModel:
    try:
        email_info = validate_email(email.email)
        email.email = email_info.normalized
        
        user = users_collection.find_one({'user_email': email.email})

        # Check if user has activated account
        if bool(user['user_activated']) != True:
            return {"message": AuthErrorMessages.INACTIVE_ACCOUNT.value, "status": status.HTTP_400_BAD_REQUEST}

        if user:
            token = generate_email_activation_token(email.email)
            email_msg = generate_forgot_password_template(token)
            if send_email("Forgot Password", email.email, email_msg) == 200:
                return {"message": AuthErrorMessages.FORGOT_PASSWORD.value, "status": status.HTTP_200_OK}
        else:
            # raise HTTPException(status_code=, detail=)
            return {"message": AuthErrorMessages.USER_NOT_FOUND.value, "status": status.HTTP_404_NOT_FOUND}
    except EmailNotValidError:
        return {"message": AuthErrorMessages.INVALID_EMAIL.value, "status": status.HTTP_406_NOT_ACCEPTABLE}
        # raise HTTPException(status_code=, detail=)