import json
from user_agents import parse
from fastapi import Response, status
from fastapi.responses import JSONResponse
from email_validator import validate_email, EmailNotValidError
# Local imports
from schemas.signin import Signin
from utils.validators import validate_ip
from utils.generators import verify_password_hash
from controller.jwt_controller import create_access_token
from utils.user_generator import create_signin_user_record
from constants.auth_error_messages import AuthErrorMessages
from database.database_connection import users_collection, users_signin_collection

async def signin_controller(user: Signin):
    
    passed_email_validation = False
    try:
        email_info = validate_email(user.email)
        user.email = email_info.normalized
        passed_email_validation = True
    except EmailNotValidError:
        return Response(AuthErrorMessages.INVALID_EMAIL.value, status.HTTP_406_NOT_ACCEPTABLE)


    if passed_email_validation:
        
        # Get user record
        user_record = users_collection.find_one({'user_email': user.email})
        if user_record:

            # Verify password
            if not verify_password_hash(user.password, user_record['user_password']):
                return Response(AuthErrorMessages.ACCOUNT_NOT_FOUND.value, status.HTTP_404_NOT_FOUND) 

            user_activated = user_record['user_activated']
            user_signup_ip = user_record['user_signup_ip']
            user_signup_device = user_record['user_signup_device']

            # Check if user account is activated
            if str(user_activated).upper() == 'False'.upper():
                return Response(AuthErrorMessages.ACCOUNT_NOT_ACTIVATED.value, status.HTTP_406_NOT_ACCEPTABLE)
            
            # Validate user IP
            if validate_ip(user.ip_address):
                if user.ip_address.upper() != str(user_signup_ip).upper():
                    # check if this IP was used previously used for signin 
                    signin_ips = [str(doc['user_signin_ip']).upper() for doc in users_signin_collection.find({'user_email': user.email}, {"user_signin_ip": 1})]
                    print(signin_ips)
                    if user.ip_address.upper() not in signin_ips:
                        # Verification email should be sent here
                        return Response(AuthErrorMessages.VERIFY_ACCOUNT.value, status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(AuthErrorMessages.INVALID_IP.value, status.HTTP_406_NOT_ACCEPTABLE)
            

            # Parse user agent 
            user_agent = parse(user.user_agent)
            if user_agent:
                user_signin_device = str(user_agent.device.family).upper()
                if user_signin_device != str(user_signup_device).upper():
                    signin_devices = [str(doc['user_signin_device']).upper() for doc in users_signin_collection.find({'user_email': user.email}, {'user_signin_device'})]
                    print(signin_devices)
                    if user_signin_device not in signin_devices:
                        # Verification email should be sent here
                        return Response(AuthErrorMessages.VERIFY_ACCOUNT.value, status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(AuthErrorMessages.INVALID_USERAGENT.value, status.HTTP_406_NOT_ACCEPTABLE)
            
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
                123.456,
                123.678
            )
            users_signin_collection.insert_one(signin_record)

            # Generate login token default expire 2 days
            login_token = create_access_token({'user_email': user.email})
            
            # Send redirection response 
            return JSONResponse({"access_token": login_token, "token_type": "bearer"}, status.HTTP_301_MOVED_PERMANENTLY)

        else:
            return Response(AuthErrorMessages.ACCOUNT_NOT_FOUND.value, status.HTTP_404_NOT_FOUND)
        

    return Response("AuthErrorMessages.NO_SIGNUP_METHOD.value", status.HTTP_406_NOT_ACCEPTABLE)