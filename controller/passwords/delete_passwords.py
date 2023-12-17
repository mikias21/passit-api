from bson import ObjectId
from fastapi import status, HTTPException

# Local imports
from constants.auth_error_messages import AuthErrorMessages
from schemas.passwords_req_res import PasswordsResponseModel
from database.database_connection import users_password_collection
from constants.password_error_message import PasswordErrorMessages

async def delete_password_controller(id: str, email: str) -> PasswordsResponseModel:
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AuthErrorMessages.LOGIN_EXPIRED.value)
    
    try:
        if id:
            password_object_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=PasswordErrorMessages.PASSWORD_NOT_FOUND.value)
    
    pass_rec = users_password_collection.find_one({"password_id": password_object_id, "owner_email": email})
    if not pass_rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=PasswordErrorMessages.PASSWORD_NOT_FOUND.value)
    
    res = users_password_collection.delete_one({"password_id": password_object_id, "owner_email": email})
    
    if res.deleted_count == 1:
        pass_rec["password_id"] = str(pass_rec["password_id"])
        return pass_rec     
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=AuthErrorMessages.LOGIN_EXPIRED.value)