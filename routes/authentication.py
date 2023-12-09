from fastapi import APIRouter, status, Response
from fastapi.responses import ORJSONResponse, JSONResponse
# Local imports
from schemas.otp import OTP
from schemas.signup import Signup
from schemas.signin import Signin
from schemas.reset_password import ResetPassword
from schemas.verify_account import VerifyAccount
from schemas.forgot_password import ForgotPassword
from controller.signup_controller import signup_controller
from controller.signin_controller import signin_controller
from controller.reset_password_controller import reset_password_controller
from controller.verify_account_controller import verify_account_controller
from controller.forgot_password_controller import forgot_password_controller
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
    response = await signin_controller(user)
    return ORJSONResponse({"msg": response.body.decode("utf-8")}, response.status_code)

@router.post('/verify/{token}', status_code=status.HTTP_301_MOVED_PERMANENTLY)
async def verify_account(token: str, account: VerifyAccount):
    response = await verify_account_controller(token, account)
    return ORJSONResponse({"msg": response.body.decode("utf-8")}, response.status_code)

@router.get('/forgot', status_code=status.HTTP_200_OK)
async def forgot_password(email: ForgotPassword):
    response = await forgot_password_controller(email)
    return ORJSONResponse({"msg": response.body.decode("utf-8")}, response.status_code)

@router.post('/reset_password/{token}', status_code=status.HTTP_201_CREATED)
async def reset_password(token: str, password: ResetPassword):
    response = await reset_password_controller(token, password)
    return ORJSONResponse({"msg": response.body.decode("utf-8")}, response.status_code)