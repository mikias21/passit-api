from password_validator import PasswordValidator
from fastapi import Response, status, HTTPException

# Local imports
from utils.generators import generate_password_hash
from database.database_connection import users_collection
from constants.auth_error_messages import AuthErrorMessages
from utils.validators import validate_email_activation_token
from schemas.reset_password import ResetPassword, ResetPasswordResponseModel

async def reset_password_controller(token: str, password: ResetPassword) -> ResetPasswordResponseModel:
    email = validate_email_activation_token(token)
    if email:
        
        password_schema = PasswordValidator()
        password_schema.min(8).max(16).has().uppercase().has().lowercase().has().digits().has().digits().has().no().spaces().has().symbols()

        user = users_collection.find_one({'user_email': email})

        if user:

            if not password_schema.validate(password.password):
                return {"message": AuthErrorMessages.INVALID_PASSWORD.value, "status": status.HTTP_406_NOT_ACCEPTABLE}
                # raise HTTPException(status_code=, detail=)
        
            if password.password.upper() != password.confirm_password.upper():
                return {"message": AuthErrorMessages.PASSWORD_NOT_MATCH.value, "status": status.HTTP_406_NOT_ACCEPTABLE}
                # raise HTTPException(status_code=, detail=)

            hashed_password = generate_password_hash(password.password)

            myquery = { "user_email": str(email) }
            newvalues = { "$set": { "user_password": hashed_password } }
            users_collection.update_one(myquery, newvalues, upsert=False)
            
            return {"message": AuthErrorMessages.PASSWORD_UPDATED.value, "status": status.HTTP_201_CREATED}

        else:
            return {"message": AuthErrorMessages.USER_NOT_FOUND.value, "status": status.HTTP_404_NOT_FOUND}
            # raise HTTPException(status_code=, detail=)

    return {"message": AuthErrorMessages.ACTIVATION_TOKEN_EXPIRED.value, "status": status.HTTP_406_NOT_ACCEPTABLE}
    # raise HTTPException(status_code=, detail=)