from pydantic import BaseModel

class VerifyAccount(BaseModel):
    otp: str
    ip_address: str
    user_agent: str

class VerifyAccountModelResponse(BaseModel):
    access_token: str
    token_type: str