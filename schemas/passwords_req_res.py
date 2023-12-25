from typing import Optional
from pydantic import BaseModel

class PasswordsResponseModel(BaseModel):
    password_id: Optional[str] = None
    label: Optional[str] = None
    password: Optional[str] = None
    category: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    owner_email: Optional[str] = None
    added_date_time: Optional[str] = None
    message: Optional[str] = None
    status: Optional[int] = None


class PasswordsRequestModel(BaseModel):
    label: str
    password: str
    category: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None