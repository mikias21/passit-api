from bson import ObjectId
from fastapi import status

# Local imports
from utils.generators import generate_plane_text
from constants.password_error_message import PasswordErrorMessages
from database.database_connection import users_password_collection

async def decrypt_password_controller(id: str, email: str):
    password_rec = users_password_collection.find_one({"password_id": ObjectId(id), "owner_email": email})
    if not password_rec:
        return {"message": PasswordErrorMessages.PASSWORD_NOT_FOUND.value, "status": status.HTTP_404_NOT_FOUND}
    plain_text = generate_plane_text(password_rec['enc_key'], password_rec['enc_iv'], password_rec['password'])
    
    return {"password": plain_text, "status": status.HTTP_200_OK}