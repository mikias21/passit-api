from bson import ObjectId
from fastapi import status
from datetime import datetime

# Local imports
from constants.auth_error_messages import AuthErrorMessages
from constants.category_error_messages import CategoryErrorMessages
from database.database_connection import users_passwords_categories
from schemas.categories_req_res import CategoriesRequestModel, CategoriesResponseModel


def add_category_controller(email: str, category: CategoriesRequestModel):
    if not email:
        return {"message": AuthErrorMessages.LOGIN_EXPIRED.value, "status": status.HTTP_401_UNAUTHORIZED}
    
    # Validate category name
    category.category_name = category.category_name.strip() if category.category_name else ""

    if category.category_name:
        if not category.category_name.isalnum():
            return {"message": CategoryErrorMessages.INVALID_CATEGORY_NAME.value, "status": status.HTTP_400_BAD_REQUEST}
        
    # Check if the same cateogry is found in db
    category_rec = users_passwords_categories.find_one({"owner_email": email, "name": category.category_name})
    
    if category_rec:
        return {"message": CategoryErrorMessages.CATEGORY_DUPLICATE.value, "status": status.HTTP_400_BAD_REQUEST} 
    
    new_password = {
        "category_id": ObjectId(),
        "name": category.category_name,
        "owner_email": email,
        'added_date_time': str(datetime.now())
    }

    result = users_passwords_categories.insert_one(new_password)

    insert_id = result.inserted_id
    inserted_doc = users_passwords_categories.find_one({"_id": insert_id})
    inserted_doc['category_id'] = str(inserted_doc['category_id'])

    return inserted_doc
