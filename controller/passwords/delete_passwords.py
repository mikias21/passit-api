from bson import ObjectId
from fastapi import status, HTTPException

# Local imports
from constants.auth_error_messages import AuthErrorMessages
from schemas.passwords_req_res import PasswordsResponseModel
from database.database_connection import users_password_collection
from constants.password_error_message import PasswordErrorMessages

async def delete_password_controller(id: str, email: str) -> PasswordsResponseModel:
    if not email:
        return {"message": AuthErrorMessages.LOGIN_EXPIRED.value, "status": status.HTTP_401_UNAUTHORIZED}
    
    try:
        if id:
            password_object_id = ObjectId(id)
    except Exception:
        return {"message": PasswordErrorMessages.PASSWORD_NOT_FOUND.value, "status": status.HTTP_404_NOT_FOUND}
    
    pass_rec = users_password_collection.find_one({"password_id": password_object_id, "owner_email": email})
    if not pass_rec:
        return {"message": PasswordErrorMessages.PASSWORD_NOT_FOUND.value, "status": status.HTTP_404_NOT_FOUND}
    
    res = users_password_collection.delete_one({"password_id": password_object_id, "owner_email": email})
    
    if res.deleted_count == 1:
        pass_rec["password_id"] = str(pass_rec["password_id"])
        return pass_rec     
    
    return {"message": AuthErrorMessages.LOGIN_EXPIRED.value, "status": status.HTTP_401_UNAUTHORIZED}