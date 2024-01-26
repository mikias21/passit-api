from bson import ObjectId
from fastapi import status

# Local imports
from constants.auth_error_messages import AuthErrorMessages
from schemas.passwords_req_res import PasswordsResponseModel
from constants.password_error_message import PasswordErrorMessages
from database.database_connection import users_password_collection

async def update_password_importance(id: str, email: str) -> PasswordsResponseModel:
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
    update_data = {
        "$set": {
            "important": not pass_rec['important']
        }
    }

    result = users_password_collection.update_one({"password_id": id, "owner_email": email}, update_data)
    if result.modified_count > 0:
        updated = users_password_collection.find_one({"password_id": id, "owner_email": email})
        updated['password_id'] = str(updated['password_id'])
        updated['password'] = str(updated['password'])
        return updated 
    
    return None