from user_agents import parse
from password_validator import PasswordValidator
from fastapi import Response, status, HTTPException
from email_validator import validate_email, EmailNotValidError
# Local import
from utils.validators import validate_ip
from utils.user_generator import create_new_user
from controller.email_controller import send_email
from utils.generators import generate_password_hash
from schemas.signup import Signup, SignupResponseModel
from database.database_connection import users_collection
from constants.auth_error_messages import AuthErrorMessages
from utils.generators import generate_user_longitude_latitude
from utils.email_template_generator import generate_account_activation_template
from utils.generators import generate_email_activation_token, generate_random_otp, get_date_time_difference

async def signup_controller(user: Signup) -> SignupResponseModel:
    # Check if either signup by email or phone is true
    if not user.is_email and not user.is_phone:
        return {"message": AuthErrorMessages.NO_SIGNUP_METHOD.value, "status": status.HTTP_406_NOT_ACCEPTABLE}

    password_schema = PasswordValidator()
    password_schema.min(8).max(16).has().uppercase().has().lowercase().has().digits().has().digits().has().no().spaces().has().symbols()
    
    # if by email
    if user.is_email:
        # Validate email
        try:
            email_info = validate_email(user.email)
            user.email = email_info.normalized
        except EmailNotValidError:
            return {"message": AuthErrorMessages.INVALID_EMAIL.value, "status": status.HTTP_406_NOT_ACCEPTABLE}
        
        # Valiate password and encrypt
        if not password_schema.validate(user.password):
            return {"message": AuthErrorMessages.INVALID_PASSWORD.value, "status": status.HTTP_406_NOT_ACCEPTABLE}
        
        # Validate IP
        if not validate_ip(user.ip_address):
            return {"message": AuthErrorMessages.INVALID_IP.value, "status": status.HTTP_406_NOT_ACCEPTABLE}
        else:
            lat, long = generate_user_longitude_latitude(user.ip_address)
        
        # Validate UserAgent
        user_agent = None
        if user.user_agent:
            # Parse User Agent
            user_agent = parse(user.user_agent)
        else:
            return {"message": AuthErrorMessages.INVALID_USERAGENT.value, "status": status.HTTP_406_NOT_ACCEPTABLE}
        
        # Check if email is already used for registeration
        old_user = users_collection.find_one({'user_email': user.email})
        if old_user:
            days_diff = get_date_time_difference(str(old_user['user_signup_datetime']))
            if str(old_user['user_activated']).upper() == 'False'.upper() and days_diff > 1:
                users_collection.delete_one({'user_email': user.email})
            else:
                return {"message": AuthErrorMessages.EMAIL_TAKEN.value, "status": status.HTTP_406_NOT_ACCEPTABLE}
        
        # send email
        otp = generate_random_otp()
        verification_token = generate_email_activation_token(user.email)
        email_message = generate_account_activation_template(verification_token, otp)
        if send_email("Activate account", user.email, email_message) == 200:
            # insert to db
            new_user = create_new_user(user.email, generate_password_hash(user.password), user.ip_address, 
                                    user_agent.browser.family, user_agent.browser.version_string,
                                    user_agent.os.family, user_agent.os.version_string,
                                    user_agent.device.family, user_agent.device.model, otp, user_lat=lat, user_long=long)
            users_collection.insert_one(new_user)
        else:
            return {"message": AuthErrorMessages.EMAIL_SENDING_ERROR, "status": status.HTTP_500_INTERNAL_SERVER_ERROR}
                
        
        return {"message": AuthErrorMessages.SIGNUP_SUCCESS.value, "status": status.HTTP_201_CREATED}


    # if by phone
        # pass