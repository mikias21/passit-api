from fastapi import Response, status
from fastapi.responses import JSONResponse

# Local imports
from schemas.verify_account import VerifyAccount
from controller.jwt_controller import create_access_token
from constants.auth_error_messages import AuthErrorMessages
from utils.validators import validate_email_activation_token
from database.database_connection import users_verify_account_record

async def verify_account_controller(token: str, account: VerifyAccount):
    email = validate_email_activation_token(token)
    if email:
        print(email)

        otp_identifier = token.rsplit('.', 1)[1]
        login_record = users_verify_account_record.find_one({'otp_identifier': otp_identifier})

        if login_record['otp_code'].upper() != account.otp.upper():
            return Response(AuthErrorMessages.INCORRECT_OTP.value, status.HTTP_406_NOT_ACCEPTABLE)

    else:
        return Response(AuthErrorMessages.ACTIVATION_TOKEN_EXPIRED.value, status.HTTP_401_UNAUTHORIZED)
    
    login_token = create_access_token({'user_email': email})
    return JSONResponse({"access_token": login_token, "token_type": "bearer"}, status.HTTP_301_MOVED_PERMANENTLY)