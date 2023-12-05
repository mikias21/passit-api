from fastapi import APIRouter, status, Response
from fastapi.responses import ORJSONResponse
# Local imports
from schemas.otp import OTP
from schemas.signup import Signup
from schemas.signin import Signin
from controller.signup_controller import signup_controller
from controller.signin_controller import signin_controller
from controller.activate_account_controller import activate_account_controller

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup_user(user: Signup):
    response: Response = await signup_controller(user)
    return ORJSONResponse({"msg": response.body.decode("utf-8")}, response.status_code)

@router.post('/activate/{token}', status_code=status.HTTP_200_OK)
async def activate_account(token: str, otp: OTP):
    response: Response = await activate_account_controller(token, otp)
    return ORJSONResponse({"msg": response.body.decode("utf-8")}, response.status_code)

@router.post('/signin', status_code=status.HTTP_301_MOVED_PERMANENTLY)
async def signin_user(user: Signin):
    print(user.email, user.password)
    response: Response = await signin_controller(user)
    return ORJSONResponse({"msg": response.body.decode("utf-8")}, response.status_code)