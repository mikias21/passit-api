from fastapi.responses import ORJSONResponse, JSONResponse
from fastapi import APIRouter, status, Response, Request, Depends, HTTPException
# Local imports
from schemas.otp import OTP
from schemas.signup import Signup, SignupResponseModel
from schemas.signin import Signin, SigninResponseModel
from schemas.activate_account import ActivateAccountResponseModel
from controller.o2auth.signup_controller import signup_controller
from controller.o2auth.signin_controller import signin_controller
from controller.o2auth.signout_controller import signout_controller
from controller.o2auth.verify_account_controller import verify_account_controller
from schemas.verify_account import VerifyAccount, VerifyAccountModelResponse
from schemas.reset_password import ResetPassword, ResetPasswordResponseModel
from schemas.forgot_password import ForgotPassword, ForgotPasswordResponseModel
from controller.o2auth.reset_password_controller import reset_password_controller
from controller.o2auth.forgot_password_controller import forgot_password_controller
from controller.o2auth.activate_account_controller import activate_account_controller

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=SignupResponseModel)
async def signup_user(user: Signup):
    response = await signup_controller(user)
    return response

@router.post('/activate/{token}', status_code=status.HTTP_200_OK, response_model=ActivateAccountResponseModel)
async def activate_account(token: str, otp: OTP):
    response = await activate_account_controller(token, otp)
    return response

@router.post('/signin', status_code=status.HTTP_200_OK, response_model=SigninResponseModel)
async def signin_user(user: Signin):
    response = await signin_controller(user)
    return response

@router.post('/verify/{token}', status_code=status.HTTP_200_OK, response_model=VerifyAccountModelResponse)
async def verify_account(token: str, account: VerifyAccount):
    response = await verify_account_controller(token, account)
    return response

@router.post('/forgot', status_code=status.HTTP_200_OK, response_model=ForgotPasswordResponseModel)
async def forgot_password(email: ForgotPassword):
    response = await forgot_password_controller(email)
    return response

@router.post('/reset_password/{token}', status_code=status.HTTP_201_CREATED, response_model=ResetPasswordResponseModel)
async def reset_password(token: str, password: ResetPassword):
    response = await reset_password_controller(token, password)
    return response

@router.get('/signout/{token}', status_code=status.HTTP_200_OK)
async def signout(token: str):
    status = signout_controller(token)
    if status == 200:
        raise HTTPException(status_code=status, detail="success")