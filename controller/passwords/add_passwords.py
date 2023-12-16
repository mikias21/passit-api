from bson import ObjectId
from datetime import datetime
from fastapi import status, HTTPException

# Local imports
from constants.auth_error_messages import AuthErrorMessages
from constants.password_error_message import PasswordErrorMessages
from database.database_connection import users_password_collection
from schemas.passwords_req_res import PasswordsRequestModel, PasswordsResponseModel

async def add_password_controller(password: PasswordsRequestModel, email: str) -> PasswordsResponseModel:
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AuthErrorMessages.LOGIN_EXPIRED.value)
    
    # Validate label
    # Validate category
    # validate url
    # validate description / comments
    new_password = dict(password)
    new_password.update({'password_id': ObjectId(), 'owner_email': email, 'added_date_time': str(datetime.now())})

    result = users_password_collection.insert_one(dict(new_password))

    insert_id = result.inserted_id
    inserted_doc = users_password_collection.find_one({"_id": insert_id})
    inserted_doc['password_id'] = str(inserted_doc['password_id'])
    
    return inserted_doc