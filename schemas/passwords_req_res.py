from typing import Optional
from pydantic import BaseModel

class PasswordsResponseModel(BaseModel):
    password_id: str
    label: str
    password: str
    category: str
    url: str
    description: str
    owner_email: str
    added_date_time: str


class PasswordsRequestModel(BaseModel):
    label: str
    password: str
    category: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None