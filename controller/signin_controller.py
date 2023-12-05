from fastapi import Response, status
# Local imports
from schemas.signin import Signin

async def signin_controller(user: Signin):
    # validate email address
    # validate IP address
        # Check if the user signin IP is similar with the signup IP
        # if not the same
        # Get the list of previous signin IP address
        # See if the current signin IP is in the list of previous IPs
        # If not the same, send account verification through email OTP
    # parse and validate user agent
        #(Check if user signin OS is similar with signup OS) 
        # If not the same
        # Get the list of previous signin signin OS
        # See if the current signin device is in the list of the previous devices
        # If not the same, send account verification through email OTP     
    # If validation pass
    # Generate required fileds
    # Add to db and generate secure session token
    # redirect response
    return Response("AuthErrorMessages.NO_SIGNUP_METHOD.value", status.HTTP_406_NOT_ACCEPTABLE)