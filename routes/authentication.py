from fastapi import APIRouter, status, Response
from fastapi.responses import ORJSONResponse
# Local imports
from schemas.signup import Signup
from controller.signup_controller import signup_controller
from controller.activate_account_controller import activate_account_controller

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup_user(user: Signup):
    response: Response = await signup_controller(user)
    return ORJSONResponse({"msg": response.body.decode("utf-8")}, response.status_code)

@router.get('/activate/{token}', status_code=status.HTTP_200_OK)
async def activate_account(token: str):
    response: Response = await activate_account_controller(token)
    return ORJSONResponse({"msg": response.body.decode("utf-8")}, response.status_code)