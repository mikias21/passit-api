from pydantic import BaseModel

class ForgotPassword(BaseModel):
    email: str
    ip_address: str
    user_agent: str