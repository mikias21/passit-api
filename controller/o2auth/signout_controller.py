from datetime import datetime
from fastapi import status, HTTPException

# Local imports
from controller.jwt_controller import verify_access_token
from database.database_connection import users_login_token_collection

def signout_controller(token: str):
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request, please try again.")
    
    email = verify_access_token(token)
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request, please try again.")

    token_details = {'email': email, 'token': token, 'logout_time': str(datetime.now())}
    
    # Check if token is not already in db to avoid multiple logout records with the same token
    tokens = users_login_token_collection.find({"email": email})
    for token_dict in tokens:
        if token_dict['token'] != token:
            try:
                result = users_login_token_collection.insert_one(token_details)
            except Exception:
                if result.inserted_id:
                    return status.HTTP_200_OK

    return status.HTTP_200_OK