from user_agents import parse
from fastapi import Response, status
from password_validator import PasswordValidator
from email_validator import validate_email, EmailNotValidError
# Local import
from schemas.signup import Signup
from utils.validators import validate_ip
from utils.user_generator import create_new_user
from database.database_connection import users_collection
from constants.auth_error_messages import AuthErrorMessages
from utils.generators import generate_email_activation_token
from utils.email_template_generator import email_template_generator
from controller.email_controller import send_email

async def signup_controller(user: Signup):
    # Check if either signup by email or phone is true
    if not user.is_email and not user.is_phone:
        return Response(AuthErrorMessages.NO_SIGNUP_METHOD.value, status.HTTP_406_NOT_ACCEPTABLE)

    password_schema = PasswordValidator()
    password_schema.min(8).max(16).has().uppercase().has().lowercase().has().digits().has().digits().has().no().spaces().has().symbols()
    
    validation_pass = True

    # if by email
    if user.is_email:
        # Validate email
        try:
            email_info = validate_email(user.email)
            user.email = email_info.normalized
        except EmailNotValidError:
            validation_pass = False
            return Response(AuthErrorMessages.INVALID_EMAIL.value, status.HTTP_406_NOT_ACCEPTABLE)
        
        # Valiate password and encrypt
        if not password_schema.validate(user.password):
            return Response(AuthErrorMessages.INVALID_PASSWORD.value, status.HTTP_406_NOT_ACCEPTABLE)
        
        # Validate IP
        if validate_ip(user.ip_address):
            # If IP valid, make api request to get location lat,long
            pass
        else:
            validation_pass = False
            return Response(AuthErrorMessages.INVALID_IP.value, status.HTTP_406_NOT_ACCEPTABLE)
        
        # Validate UserAgent
        user_agent = None
        if user.user_agent:
            # Parse User Agent
            user_agent = parse(user.user_agent)
        else:
            validation_pass = False
            return Response(AuthErrorMessages.INVALID_USERAGENT.value, status.HTTP_406_NOT_ACCEPTABLE)
        
        # Check if email is already used for registeration
        old_user = users_collection.find_one({'user_email': user.email})
        if old_user:
            return Response(AuthErrorMessages.EMAIL_TAKEN.value, status.HTTP_406_NOT_ACCEPTABLE)
        
        # send email
        if validation_pass: 
            verification_token = generate_email_activation_token(user.email)
            email_message = email_template_generator(verification_token)
            if send_email("Activate account", user.email, email_message) == 200:
                # insert to db
                new_user = create_new_user(user.email, user.password, user.ip_address, 
                                        user_agent.browser.family, user_agent.browser.version_string,
                                        user_agent.os.family, user_agent.os.version_string,
                                        user_agent.device.family, user_agent.device.model, 123.456, 123.678)
                users_collection.insert_one(new_user)
            else:
                return Response(AuthErrorMessages.EMAIL_SENDING_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(AuthErrorMessages.SIGNUP_SUCCESS.value, status.HTTP_201_CREATED)


    # if by phone
        # pass