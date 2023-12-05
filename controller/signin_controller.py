from fastapi import Response, status
# Local imports
from schemas.signin import Signin

async def signin_controller(user: Signin):
    # Check if either signup by email or phone is true
    if not user.is_email and not user.is_phone:
        return Response("AuthErrorMessages.NO_SIGNUP_METHOD.value", "status.HTTP_406_NOT_ACCEPTABLE")