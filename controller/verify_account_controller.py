from fastapi import Response, status

# Local imports
from schemas.verify_account import VerifyAccount
from utils.validators import validate_email_activation_token
from constants.auth_error_messages import AuthErrorMessages

async def verify_account_controller(account: VerifyAccount):
    email = validate_email_activation_token(account.token)
    if email:
        print(email)

        # Get otp identifier by spliting curr token

        # Get record from db

        # validate OTP

        # Generate session token

    else:
        return Response(AuthErrorMessages.ACTIVATION_TOKEN_EXPIRED, status.HTTP_401_UNAUTHORIZED)
    
    return Response("Testing", status.HTTP_301_MOVED_PERMANENTLY)