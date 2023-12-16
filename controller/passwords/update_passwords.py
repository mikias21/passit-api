from bson import ObjectId
from fastapi import status, HTTPException

# Local imports
from utils.validators import validate_url
from constants.auth_error_messages import AuthErrorMessages
from constants.password_error_message import PasswordErrorMessages
from database.database_connection import users_password_collection
from utils.generators import generate_encoded_url, generate_clean_input
from schemas.passwords_req_res import PasswordsResponseModel, PasswordsRequestModel

async def update_password_controller(id: str, email: str, password: PasswordsRequestModel) -> PasswordsResponseModel:
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AuthErrorMessages.LOGIN_EXPIRED.value)
    
    if not id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=PasswordErrorMessages.PASSWORD_NOT_FOUND.value)
    
    id = ObjectId(id)
        
    # Validate label
    if not password.label.isalnum() or len(password.label.strip()) > 20:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=PasswordErrorMessages.INVALID_LABEL.value)
    
    # Validate category
    if password.category is None:
        password.category = "main"
    elif not password.category.isalnum() or len(password.category.strip()) > 20:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=PasswordErrorMessages.INVALID_LABEL.value)
    
    # validate url
    if not validate_url(password.url.strip()):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=PasswordErrorMessages.INVALID_URL.value)
    else:
        password.url = generate_encoded_url(password.url)

    # validate description / comments
    password.description = generate_clean_input(password.description)

    update_data = {
        "$set": {
            "label": password.label.strip(),
            "password": password.password,
            "category": password.category,
            "url": password.url,
            "description": password.description
        }
    }

    result = users_password_collection.update_one({"password_id": id, "owner_email": email}, update_data)

    if result.modified_count > 0:
        updated = users_password_collection.find_one({"password_id": id, "owner_email": email})
        updated['password_id'] = str(updated['password_id'])
        return updated 
    
    return None