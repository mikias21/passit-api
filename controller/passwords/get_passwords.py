from bson import ObjectId
from fastapi import status, HTTPException

# Local imports
from constants.auth_error_messages import AuthErrorMessages
from schemas.passwords_req_res import PasswordsResponseModel
from database.database_connection import users_password_collection

async def get_passwords_controller(email: str) -> list[PasswordsResponseModel]:
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=AuthErrorMessages.LOGIN_EXPIRED.value)
    
    user_passwords = users_password_collection.find({"owner_email": email})
    user_passwords_list = list(user_passwords)
    for password in user_passwords_list:
        password['password_id'] = str(password['password_id'])

    return user_passwords_list

async def get_password_controller(email: str, password_id: str) -> PasswordsResponseModel:
    if not email:
        raise HTTPException()
    
    password = users_password_collection.find_one({"owner_email":email, "password_id": ObjectId(password_id)})
    password['password_id'] = str(password['password_id'])
    return password