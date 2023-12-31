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
        return {"message": AuthErrorMessages.LOGIN_EXPIRED.value, "status": status.HTTP_401_UNAUTHORIZED}
    
    if not id:
        return {"message": PasswordErrorMessages.PASSWORD_NOT_FOUND.value, "status": status.HTTP_404_NOT_FOUND}
    
    try:
        id = ObjectId(id)
    except Exception:
        return {"message": PasswordErrorMessages.PASSWORD_NOT_FOUND.value, "status": status.HTTP_404_NOT_FOUND}
    

    pass_rec = users_password_collection.find_one({"password_id": id, "owner_email": email})

    # Validate label
    if len(password.label.strip()) > 0:
        if not password.label.isalnum() or len(password.label.strip()) > 20:
            return {"message": PasswordErrorMessages.INVALID_LABEL.value, "status": status.HTTP_406_NOT_ACCEPTABLE}
    
    # Validate category
    if password.category is None or len(password.category.strip()):
        password.category = "main"
    
    # validate url
    if len(password.url.strip()) > 50:
        return {"message": PasswordErrorMessages.URL_LENGTH_EXCEEDED.value, "status": status.HTTP_406_NOT_ACCEPTABLE}
    if password.url and not validate_url(password.url.strip()):
        return {"message": PasswordErrorMessages.INVALID_URL.value, "status": status.HTTP_406_NOT_ACCEPTABLE}
    elif password.url:
        password.url = generate_encoded_url(password.url)

    # validate description / comments
    if password.description:
        password.description = generate_clean_input(password.description)

    update_data = {
        "$set": {
            "label": password.label.strip() if len(password.label.strip()) > 0 else pass_rec['label'],
            "password": password.password if len(password.password.strip()) > 0 else pass_rec['password'],
            "category": password.category if password.category.strip().upper() == 'main'.upper() else 'main',
            "url": password.url if len(password.url.strip()) > 0 else pass_rec['url'],
            "description": password.description if len(password.description.strip()) > 0 else pass_rec['description']
        }
    }

    result = users_password_collection.update_one({"password_id": id, "owner_email": email}, update_data)

    if result.modified_count > 0:
        updated = users_password_collection.find_one({"password_id": id, "owner_email": email})
        updated['password_id'] = str(updated['password_id'])
        updated['password'] = str(updated['password'])
        return updated 
    
    return None