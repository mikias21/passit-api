from fastapi import status, HTTPException

# Local imports
from controller.jwt_controller import create_access_token
from constants.auth_error_messages import AuthErrorMessages
from utils.validators import validate_email_activation_token
from database.database_connection import users_verify_account_record
from schemas.verify_account import VerifyAccount, VerifyAccountModelResponse

async def verify_account_controller(token: str, account: VerifyAccount) -> VerifyAccountModelResponse:
    email = validate_email_activation_token(token)
    if email:
        otp_identifier = token.rsplit('.', 1)[1]
        login_record = users_verify_account_record.find_one({'otp_identifier': otp_identifier})

        if login_record['otp_code'].upper() != account.otp.upper():
            return {"message": AuthErrorMessages.INCORRECT_OTP.value, "status": status.HTTP_406_NOT_ACCEPTABLE}

    else:
        return {"message": AuthErrorMessages.ACTIVATION_TOKEN_EXPIRED.value, "status": status.HTTP_401_UNAUTHORIZED}
    
    login_token = create_access_token({'user_email': email})
    return {"access_token": login_token, "token_type": "bearer", "status": status.HTTP_200_OK}