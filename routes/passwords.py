from fastapi import Header
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, status, Depends, HTTPException

# Local imports
from controller.jwt_controller import verify_access_token
from constants.password_error_message import PasswordErrorMessages
from controller.passwords.add_passwords import add_password_controller
from controller.passwords.update_passwords import update_password_controller
from controller.passwords.decrypt_password import decrypt_password_controller
from controller.passwords.update_password_importance import update_password_importance
from controller.passwords.update_password_starred import update_password_starred_controller
from controller.passwords.get_passwords import get_passwords_controller, get_password_controller, get_deleted_passwords_controller
from schemas.passwords_req_res import PasswordsResponseModel, PasswordsRequestModel, PasswordLabelRequest, DecryptedPasswordModelResponse
from controller.passwords.delete_passwords import delete_password_controller, restore_password_controller, delete_password_forever_controller

router = APIRouter(prefix='/passwords')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='signin')

@router.get('/', status_code=status.HTTP_200_OK, response_model=list[PasswordsResponseModel])
async def get_passwords(token: str = Depends(oauth2_scheme)):
    email = verify_access_token(token)
    data = await get_passwords_controller(email)
    return data
    

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=PasswordsResponseModel)
async def get_password(id: str, token: str = Depends(oauth2_scheme)):
    email = verify_access_token(token)
    data = await get_password_controller(email, id)
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=PasswordErrorMessages.PASSWORD_NOT_FOUND.value)
    return data

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PasswordsResponseModel)
async def add_password(password: PasswordsRequestModel, token: str = Depends(oauth2_scheme)):
    email = verify_access_token(token)
    data = await add_password_controller(password, email)
    return data

@router.put('/{id}', status_code=status.HTTP_201_CREATED, response_model=PasswordsResponseModel)
async def update_password(id: str, password: PasswordsRequestModel, token: str = Depends(oauth2_scheme)):
    email = verify_access_token(token)
    data = await update_password_controller(id, email, password)
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=PasswordErrorMessages.PASSWORD_NOT_FOUND.value)
    return data

@router.delete('/{id}', status_code=status.HTTP_200_OK, response_model=PasswordsResponseModel)
async def delete_password(id: str, label: PasswordLabelRequest, token: str = Depends(oauth2_scheme)):
    email = verify_access_token(token)
    data = await delete_password_controller(id, email, label)
    return data

@router.get('/view/{id}', status_code=status.HTTP_200_OK, response_model=DecryptedPasswordModelResponse)
async def decrypt_password(id: str, token: str = Depends(oauth2_scheme)):
    email = verify_access_token(token)
    data = await decrypt_password_controller(id, email)
    return data

@router.get('/important/{id}/{token}', status_code=status.HTTP_201_CREATED, response_model=PasswordsResponseModel)
async def important_password(id: str, token: str):
    email = verify_access_token(token)
    data = await update_password_importance(id, email)
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=PasswordErrorMessages.PASSWORD_NOT_FOUND.value)
    return data

@router.get('/deleted/', status_code=status.HTTP_200_OK, response_model=list[PasswordsResponseModel])
async def deleted_passwords(token: str = Depends(oauth2_scheme)):
    email = verify_access_token(token)
    data = await get_deleted_passwords_controller(email)
    return data

@router.put('/deleted/restore/{id}/{token}', status_code=status.HTTP_201_CREATED, response_model=PasswordsResponseModel)
async def restore_password(id: str, token: str):
    email = verify_access_token(token)
    data = await restore_password_controller(id, email)
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=PasswordErrorMessages.PASSWORD_NOT_FOUND.value)
    return data

@router.delete('/deleted/delete/{id}/{token}', status_code=status.HTTP_200_OK, response_model=PasswordsResponseModel)
async def delete_password_forever(id: str, label: PasswordLabelRequest, token: str):
    email = verify_access_token(token)
    data = await delete_password_forever_controller(id, email, label)
    return data

@router.put('/starred/{id}/{token}', status_code=status.HTTP_201_CREATED, response_model=PasswordsResponseModel)
async def starred_password(id: str, token: str):
    email = verify_access_token(token)
    data = await update_password_starred_controller(id, email)
    return data