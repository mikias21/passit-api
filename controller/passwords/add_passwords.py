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
from database.database_connection import users_password_collection, users_collection

async def add_password_controller(password: PasswordsRequestModel, email: str) -> PasswordsResponseModel:
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AuthErrorMessages.LOGIN_EXPIRED.value)
    
    # Validate label
    if not password.label.isalnum() or len(password.label.strip()) > 20:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=PasswordErrorMessages.INVALID_LABEL.value)
    # Check if Label is not already used
    pass_rec = users_password_collection.find_one({"label": password.label})
    if pass_rec:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=PasswordErrorMessages.LABEL_USED.value)

    # Validate category
    if password.category is None:
        password.category = "main"
    elif not password.category.isalnum() or len(password.category.strip()) > 20:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=PasswordErrorMessages.INVALID_LABEL.value)
    # Check if category is not used already or use category which is not found

    # validate url
    if password.url and not validate_url(password.url.strip()):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=PasswordErrorMessages.INVALID_URL.value)
    elif password.url:
        password.url = generate_encoded_url(password.url.strip())

    # validate description / comments
    if password.description:
        password.description = generate_clean_input(password.description)

    # Encrypt password
    user_rec = users_collection.find_one({"user_email": email})
    if not user_rec:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AuthErrorMessages.LOGIN_EXPIRED.value)
    
    key, iv, cyphered = generate_encrypted_text(password.password, email)
    new_password = dict(password)
    new_password.update({'password': Binary(cyphered), 'enc_key': Binary(key), 'enc_iv': iv, 'password_id': ObjectId(), 'owner_email': email, 'added_date_time': str(datetime.now())})

    result = users_password_collection.insert_one(new_password)

    insert_id = result.inserted_id
    inserted_doc = users_password_collection.find_one({"_id": insert_id})
    inserted_doc['password_id'] = str(inserted_doc['password_id'])
    inserted_doc['password'] = password.password
    
    return inserted_doc