from fastapi import APIRouter, status

# Local imports
from schemas.passwords_response import PasswordsResponseModel

router = APIRouter(prefix='/passwords')

@router.get('/', status_code=status.HTTP_200_OK, response_model=list[PasswordsResponseModel])
def get_passwords():
    pass

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=PasswordsResponseModel)
def get_password():
    pass

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PasswordsResponseModel)
def add_password():
    pass

@router.put('/{id}', status_code=status.HTTP_201_CREATED, response_model=PasswordsResponseModel)
def update_password():
    pass

@router.delete('/{id}', status_code=status.HTTP_200_OK, response_model=PasswordsResponseModel)
def delete_password():
    pass
