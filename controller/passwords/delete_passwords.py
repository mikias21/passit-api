from bson import ObjectId
from fastapi import status, HTTPException

# Local imports
from constants.auth_error_messages import AuthErrorMessages
from database.database_connection import users_password_collection
from constants.password_error_message import PasswordErrorMessages
from schemas.passwords_req_res import PasswordsResponseModel, PasswordLabelRequest

async def delete_password_controller(id: str, email: str, label: PasswordLabelRequest) -> PasswordsResponseModel:
    if not email:
        return {"message": AuthErrorMessages.LOGIN_EXPIRED.value, "status": status.HTTP_401_UNAUTHORIZED}
    
    try:
        if id:
            password_object_id = ObjectId(id)
    except Exception:
        return {"message": PasswordErrorMessages.PASSWORD_NOT_FOUND.value, "status": status.HTTP_404_NOT_FOUND}
    
    pass_rec = users_password_collection.find_one({"password_id": ObjectId(password_object_id), "owner_email": email})
    if not pass_rec:
        return {"message": PasswordErrorMessages.PASSWORD_NOT_FOUND.value, "status": status.HTTP_404_NOT_FOUND}
    
    if label.label.strip().upper() != pass_rec['label'].upper():
        return {"message": PasswordErrorMessages.CONFIRM_PASSWORD_LABEL.value, "status": status.HTTP_400_BAD_REQUEST}
    
    res = users_password_collection.delete_one({"password_id": password_object_id, "owner_email": email})
    
    if res.deleted_count == 1:
        pass_rec['password_id'] = str(pass_rec['password_id'])
        pass_rec['password'] = str(pass_rec['password'])
        pass_rec['enc_key'] = str(pass_rec['enc_key'])
        return pass_rec     
    
    return {"message": AuthErrorMessages.LOGIN_EXPIRED.value, "status": status.HTTP_401_UNAUTHORIZED}