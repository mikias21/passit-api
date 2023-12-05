from datetime import datetime
from fastapi import Response, status
# Local imports
from schemas.otp import OTP
from utils.generators import get_date_time_difference
from database.database_connection import users_collection
from constants.auth_error_messages import AuthErrorMessages
from utils.validators import validate_email_activation_token

async def activate_account_controller(token: str, otp: OTP):
    email = validate_email_activation_token(token)
    if email:
        user = users_collection.find_one({'user_email': email})
        if user:
            days_diff = get_date_time_difference(str(user['user_signup_datetime']))
            if days_diff <= 1:
                myquery = { "user_email": str(email) }
                newvalues = { "$set": { "user_activated": "True" } }
                users_collection.update_one(myquery, newvalues, upsert=False)
                return Response(AuthErrorMessages.ACCOUNT_ACTIVATED.value, status.HTTP_200_OK)
            else:
                return Response(AuthErrorMessages.ACTIVATION_TOKEN_EXPIRED.value, status.HTTP_401_UNAUTHORIZED)
    return Response(AuthErrorMessages.ACTIVATION_TOKEN_EXPIRED.value, status.HTTP_401_UNAUTHORIZED)