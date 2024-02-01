from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, status, Depends, HTTPException

# Local imports
from controller.jwt_controller import verify_access_token
from constants.category_error_messages import CategoryErrorMessages
from controller.categories.add_categories import add_category_controller
from schemas.categories_req_res import CategoriesRequestModel, CategoriesResponseModel
from controller.categories.get_categories import get_categories_controller, get_category_controller

router = APIRouter(prefix='/categories')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='signin')

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=CategoriesResponseModel)
async def get_category(id: str, token: str = Depends(oauth2_scheme)):
    email = verify_access_token(token)
    data = await get_category_controller(email, id)
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=CategoryErrorMessages.CATEGORY_NOT_FOUND.value)
    return data

@router.get('/', status_code=status.HTTP_200_OK, response_model=list[CategoriesResponseModel])
async def get_categories(token: str = Depends(oauth2_scheme)):
    email = verify_access_token(token)
    data = await get_categories_controller(email)
    return data

@router.post('/{token}', status_code=status.HTTP_201_CREATED, response_model=CategoriesResponseModel)
async def add_category(category: CategoriesRequestModel, token: str):
    email = verify_access_token(token)
    data =  add_category_controller(email, category)
    return data