from datetime import datetime
from fastapi import Response, status, HTTPException
# Local imports
from schemas.otp import OTP
from utils.generators import get_date_time_difference
from database.database_connection import users_collection
from constants.auth_error_messages import AuthErrorMessages
from utils.validators import validate_email_activation_token
from schemas.activate_account import ActivateAccountResponseModel

async def activate_account_controller(token: str, otp: OTP) -> ActivateAccountResponseModel:
    email = validate_email_activation_token(token)
    if email:
        user = users_collection.find_one({'user_email': email})
        if user:
            days_diff = get_date_time_difference(str(user['user_signup_datetime']))
            if days_diff <= 1:
                # Check if the OTP code matches
                if user['user_signup_otp'] != otp.otp:
                    return {"message": AuthErrorMessages.INCORRECT_OTP.value, "status": status.HTTP_400_BAD_REQUEST}
                myquery = { "user_email": str(email) }
                newvalues = { "$set": { "user_activated": "True" } }
                users_collection.update_one(myquery, newvalues, upsert=False)
                return {"message": AuthErrorMessages.ACCOUNT_ACTIVATED.value, "status": status.HTTP_200_OK}
            else:
                return {"message": AuthErrorMessages.ACTIVATION_TOKEN_EXPIRED.value, "status": status.HTTP_401_UNAUTHORIZED}
                # raise HTTPException(status_code=, detail=)
            
    return {"message": AuthErrorMessages.ACTIVATION_TOKEN_EXPIRED.value, "status":status.HTTP_401_UNAUTHORIZED}