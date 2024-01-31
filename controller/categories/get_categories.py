from fastapi import status

# Local imports
from constants.auth_error_messages import AuthErrorMessages
from database.database_connection import users_passwords_categories

async def get_categories_controller(email: str):
    if not email:
        return [{"message": AuthErrorMessages.LOGIN_EXPIRED.value, "status": status.HTTP_401_UNAUTHORIZED}]
    categories = users_passwords_categories.find({"owner_email": email})

    categories = list(categories)
    for category in categories:
        category['category_id'] = str(category['category_id'])
    return categories

async def get_category_controller(email: str, id: str):
    pass