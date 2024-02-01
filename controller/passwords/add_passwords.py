from datetime import datetime
from bson import ObjectId, Binary
from fastapi import status, HTTPException

# Local imports
from utils.validators import validate_url
from constants.auth_error_messages import AuthErrorMessages
from constants.password_error_message import PasswordErrorMessages
from utils.generators import generate_encoded_url, generate_clean_input
from utils.generators import generate_encrypted_text, generate_plane_text
from schemas.passwords_req_res import PasswordsRequestModel, PasswordsResponseModel
from database.database_connection import users_password_collection, users_collection, users_passwords_categories

async def add_password_controller(password: PasswordsRequestModel, email: str) -> PasswordsResponseModel:
    if not email:
        return {"message": AuthErrorMessages.LOGIN_EXPIRED.value, "status": status.HTTP_401_UNAUTHORIZED}
    
    # Validate label
    if not password.label.isalnum() or len(password.label.strip()) > 20:
        return {"message": PasswordErrorMessages.INVALID_LABEL.value, "status": status.HTTP_406_NOT_ACCEPTABLE}
    # Check if Label is not already used
    pass_rec = users_password_collection.find_one({"label": password.label, "owner_email": email})
    if pass_rec:
        return {"message": PasswordErrorMessages.LABEL_USED.value, "status": status.HTTP_406_NOT_ACCEPTABLE}

    # Validate category
    if password.category is None:
        password.category = "main"
    elif not password.category.isalnum() or len(password.category.strip()) > 20:
        return {"message": PasswordErrorMessages.INVALID_LABEL.value, "status": status.HTTP_406_NOT_ACCEPTABLE}
    elif password.category.isalnum() and len(password.category.strip()) > 20:
        category_rec = users_passwords_categories.find_one({"name": password.category, "owner_email": email})
        if category_rec:
            return {"message": PasswordErrorMessages.CATEGORY_NOT_FOUND.value, "status": status.HTTP_406_NOT_ACCEPTABLE}

    # Check if category is not used already or use category which is not found 

    # validate url
    if len(password.url.strip()) > 50:
        return {"message": PasswordErrorMessages.URL_LENGTH_EXCEEDED.value, "status": status.HTTP_406_NOT_ACCEPTABLE}
    if password.url and not validate_url(password.url.strip()):
        return {"message": PasswordErrorMessages.INVALID_URL.value, "status": status.HTTP_406_NOT_ACCEPTABLE}
    elif password.url:
        password.url = generate_encoded_url(password.url.strip())

    # validate description / comments
    if password.description:
        password.description = generate_clean_input(password.description)

    # Encrypt password
    user_rec = users_collection.find_one({"user_email": email})
    if not user_rec:
        return {"message": AuthErrorMessages.LOGIN_EXPIRED.value, "status": status.HTTP_401_UNAUTHORIZED}
    
    key, iv, cyphered = generate_encrypted_text(password.password, email)
    new_password = dict(password)
    new_password.update({'password': Binary(cyphered), 'enc_key': Binary(key), 'enc_iv': iv, 'password_id': ObjectId(), 'important': False, 'starred': False, 'owner_email': email, 'added_date_time': str(datetime.now())})

    result = users_password_collection.insert_one(new_password)

    insert_id = result.inserted_id
    inserted_doc = users_password_collection.find_one({"_id": insert_id})
    inserted_doc['password_id'] = str(inserted_doc['password_id'])
    inserted_doc['password'] = password.password
    
    return inserted_doc