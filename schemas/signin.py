from typing import Optional
from pydantic import BaseModel

class Signin(BaseModel):
    email: str
    password: str
    ip_address: str
    user_agent: str

class SigninResponseModel(BaseModel):
    message: Optional[str] = None
    status: Optional [int] = None
    access_token: Optional[str] = None
    token_type: Optional[str] = None

