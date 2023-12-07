from pydantic import BaseModel

class VerifyAccount(BaseModel):
    token: str
    otp: str
    ip_address: str
    user_agent: str