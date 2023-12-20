from typing import Optional
from pydantic import BaseModel

class VerifyAccount(BaseModel):
    otp: str
    ip_address: str
    user_agent: str

class VerifyAccountModelResponse(BaseModel):
    message: Optional[str] = None
    status: Optional [int] = None
    access_token: Optional[str] = None
    token_type: Optional[str] = None