from fastapi import Response, status
# Local imports
from database.database_connection import users_collection
from constants.auth_error_messages import AuthErrorMessages
from utils.validators import validate_email_activation_token

async def activate_account_controller(token: str):
    email = validate_email_activation_token(token)
    if email:
        user = users_collection.find_one({'user_email': email})
        print(user)
        if user:
            myquery = { "user_email": str(email) }
            newvalues = { "$set": { "user_activated": "True" } }
            users_collection.update_one(myquery, newvalues, upsert=False)
            return Response(AuthErrorMessages.ACCOUNT_ACTIVATED.value, status.HTTP_200_OK)
    return Response(AuthErrorMessages.ACTIVATION_TOKEN_EXPIRED.value, status.HTTP_401_UNAUTHORIZED)