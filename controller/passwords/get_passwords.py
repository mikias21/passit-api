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
        return [{"message": AuthErrorMessages.LOGIN_EXPIRED.value, "status": status.HTTP_401_UNAUTHORIZED}]
    
    user_passwords = users_password_collection.find({"owner_email": email})
    user_passwords_list = list(user_passwords)
    for password in user_passwords_list:
        password['password_id'] = str(password['password_id'])
        password['password'] = str(password['password'])

    return user_passwords_list

async def get_password_controller(email: str, password_id: str) -> PasswordsResponseModel:
    if not email:
        return {"message": AuthErrorMessages.LOGIN_EXPIRED.value, "status": status.HTTP_401_UNAUTHORIZED}
    
    try:
        if password_id:
            password_id = ObjectId(password_id)
    except Exception:
        return {"message": PasswordErrorMessages.PASSWORD_NOT_FOUND.value, "status": status.HTTP_404_NOT_FOUND}

    password = users_password_collection.find_one({"owner_email":email, "password_id": ObjectId(password_id)})
    password['password_id'] = str(password['password_id'])
    decrypted_password = generate_plane_text(password['enc_key'], password['enc_iv'], password['password'])
    password['password'] = decrypted_password

    return password