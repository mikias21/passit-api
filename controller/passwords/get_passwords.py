from bson import ObjectId
from fastapi import status, HTTPException

# Local imports
from utils.generators import generate_plane_text
from constants.password_error_message import PasswordErrorMessages
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
    
    try:
        if password_id:
            password_id = ObjectId(password_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=PasswordErrorMessages.PASSWORD_NOT_FOUND.value)

    password = users_password_collection.find_one({"owner_email":email, "password_id": ObjectId(password_id)})
    password['password_id'] = str(password['password_id'])
    decrypted_password = generate_plane_text(password['enc_key'], password['enc_iv'], password['password'])
    password['password'] = decrypted_password

    return password