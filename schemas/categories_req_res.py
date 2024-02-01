from typing import Optional
from pydantic import BaseModel

class CategoriesRequestModel(BaseModel):
    category_name: str

class CategoriesResponseModel(BaseModel):
    category_id:  Optional[str] = None
    name:  Optional[str] = None
    owner_email:  Optional[str] = None
    added_date_time: Optional[str] = None
    message: Optional[str] = None
    status: Optional[int] = None