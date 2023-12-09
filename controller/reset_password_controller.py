from fastapi import Response, status
from password_validator import PasswordValidator

# Local imports
from schemas.reset_password import ResetPassword
from utils.generators import generate_password_hash
from database.database_connection import users_collection
from constants.auth_error_messages import AuthErrorMessages
from utils.validators import validate_email_activation_token

async def reset_password_controller(token: str, password: ResetPassword):
    email = validate_email_activation_token(token)
    if email:
        
        password_schema = PasswordValidator()
        password_schema.min(8).max(16).has().uppercase().has().lowercase().has().digits().has().digits().has().no().spaces().has().symbols()

        user = users_collection.find_one({'user_email': email})

        if user:

            if not password_schema.validate(password.password):
                return Response(AuthErrorMessages.INVALID_PASSWORD.value, status.HTTP_406_NOT_ACCEPTABLE)
        
            if password.password.upper() != password.confirm_password.upper():
                return Response(AuthErrorMessages.PASSWORD_NOT_MATCH.value, status.HTTP_406_NOT_ACCEPTABLE)
            
            hashed_password = generate_password_hash(password.password)

            myquery = { "user_email": str(email) }
            newvalues = { "$set": { "user_password": hashed_password } }
            users_collection.update_one(myquery, newvalues, upsert=False)
            
            return Response(AuthErrorMessages.PASSWORD_UPDATED.value, status.HTTP_201_CREATED)

        else:
            return Response(AuthErrorMessages.USER_NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

    
    return Response(AuthErrorMessages.ACTIVATION_TOKEN_EXPIRED.value, status.HTTP_406_NOT_ACCEPTABLE)