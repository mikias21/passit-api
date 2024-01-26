import json
from user_agents import parse
from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from email_validator import validate_email, EmailNotValidError
# Local imports
from utils.validators import validate_ip
from controller.email_controller import send_email
from schemas.signin import Signin, SigninResponseModel
from controller.jwt_controller import create_access_token
from constants.auth_error_messages import AuthErrorMessages
from utils.generators import generate_user_longitude_latitude
from models.user_account_verification_model import UserAccountVerificationModel
from utils.email_template_generator import generate_account_verification_template
from utils.user_generator import create_signin_user_record, create_account_verification_record
from database.database_connection import users_collection, users_signin_collection, users_verify_account_record
from utils.generators import verify_password_hash, generate_email_activation_token, generate_random_otp, generate_user_longitude_latitude

async def signin_controller(user: Signin) -> SigninResponseModel:
    
    passed_email_validation = False
    try:
        email_info = validate_email(user.email)
        user.email = email_info.normalized
        passed_email_validation = True
    except EmailNotValidError:
        return {"message": AuthErrorMessages.INVALID_EMAIL.value, "status": status.HTTP_406_NOT_ACCEPTABLE}
        # raise HTTPException(status_code=, detail=)


    if passed_email_validation:
        
        # Get user record
        user_record = users_collection.find_one({'user_email': user.email})
        if user_record:

            # Verify password
            if not verify_password_hash(user.password, user_record['user_password']):
                return {"message": AuthErrorMessages.ACCOUNT_NOT_FOUND.value, "status": status.HTTP_404_NOT_FOUND}
                # raise HTTPException(status_code=, detail=)

            user_activated = user_record['user_activated']
            user_signup_ip = user_record['user_signup_ip']
            user_signup_device = user_record['user_signup_device']

            # Check if user account is activated
            if str(user_activated).upper() == 'False'.upper():
                return {"message": AuthErrorMessages.ACCOUNT_NOT_ACTIVATED.value, "status": status.HTTP_406_NOT_ACCEPTABLE}
                # raise HTTPException(status_code=, detail=)
            
            # Parse user agent 
            user_agent = parse(user.user_agent)
            # This block of code needs more validation and checks have a lot of bug
            # if user_agent:
            #     user_signin_device = str(user_agent.device.family).upper()
            #     if user_signin_device != str(user_signup_device).upper():
            #         signin_devices = [str(doc['user_signin_device']).upper() for doc in users_signin_collection.find({'user_email': user.email}, {'user_signin_device'})]
            #         if user_signin_device not in signin_devices:

            #             # Verification email should be sent here
            #             verification_token = generate_email_activation_token(user.email)
            #             otp_code = generate_random_otp()
            #             otp_identifier = verification_token.rsplit('.', 1)[1]
            #             record = create_account_verification_record(
            #                 user.email, verification_token, otp_code, user.ip_address,
            #                 user_agent.browser.family, user_agent.browser.version_string,
            #                 user_agent.os.family, user_agent.os.version_string, user_agent.device.family,
            #                 user_agent.device.model, 123.456, 123.678, otp_identifier
            #             )
            #             users_verify_account_record.insert_one(record)

            #             # Send email with OTP for verification
            #             email_message = generate_account_verification_template(verification_token, otp_code)
            #             if send_email("Verify Account", user.email, email_message) == 200:
            #                 return {"message": AuthErrorMessages.VERIFY_ACCOUNT.value, "status": status.HTTP_401_UNAUTHORIZED}
            #                 # raise HTTPException(status_code=, detail=)
            # else:
            #     return {"message": AuthErrorMessages.INVALID_USERAGENT.value, "status": status.HTTP_406_NOT_ACCEPTABLE}
            
            # Validate user IP
            if validate_ip(user.ip_address):
                lat, long = generate_user_longitude_latitude(user.ip_address)
                if user.ip_address.upper() != str(user_signup_ip).upper():
                    # check if this IP was used previously used for signin 
                    signin_ips = [str(doc['user_signin_ip']).upper() for doc in users_signin_collection.find({'user_email': user.email}, {"user_signin_ip": 1})]
                    if user.ip_address.upper() not in signin_ips:
        
                        # Verification email should be sent here
                        verification_token = generate_email_activation_token(user.email)
                        otp_code = generate_random_otp()
                        otp_identifier = verification_token.rsplit('.', 1)[1]
                        record = create_account_verification_record(
                            user.email, verification_token, otp_code, user.ip_address,
                            user_agent.browser.family, user_agent.browser.version_string,
                            user_agent.os.family, user_agent.os.version_string, user_agent.device.family,
                            user_agent.device.model, lat, long, otp_identifier
                        )
                        users_verify_account_record.insert_one(record)

                        # Send email with OTP for verification
                        email_message = generate_account_verification_template(verification_token, otp_code)
                        if send_email("Verify Account", user.email, email_message) == 200:
                            return {"message": AuthErrorMessages.VERIFY_ACCOUNT.value, "status": status.HTTP_401_UNAUTHORIZED}
                            # raise HTTPException(status_code=, detail=)
                    
            else:
                return {"message": AuthErrorMessages.INVALID_IP.value, "status": status.HTTP_406_NOT_ACCEPTABLE}
            
            # add user to db
            signin_record = create_signin_user_record(
                user.email,
                user.ip_address,
                user_agent.browser.family,
                user_agent.browser.version_string,
                user_agent.os.family,
                user_agent.os.version_string,
                user_agent.device.family,
                user_agent.device.model,
                lat,
                long
            )
            users_signin_collection.insert_one(signin_record)

            # Generate login token default expire 2 days
            login_token = create_access_token({'user_email': user.email})
            
            # Send redirection response
            return {"access_token": login_token, "token_type": "bearer", "status": status.HTTP_200_OK}

        else:
            return {"message": AuthErrorMessages.ACCOUNT_NOT_FOUND.value, "status": status.HTTP_404_NOT_FOUND}
            # raise HTTPException(status_code=, detail=)
        