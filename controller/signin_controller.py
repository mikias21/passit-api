from fastapi import Response, status
# Local imports
from schemas.signin import Signin

async def signin_controller(user: Signin):
    
    return Response("AuthErrorMessages.NO_SIGNUP_METHOD.value", status.HTTP_406_NOT_ACCEPTABLE)