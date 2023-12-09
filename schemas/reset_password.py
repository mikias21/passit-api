from pydantic import BaseModel

class ResetPassword(BaseModel):
    password: str
    confirm_password: str
    ip_address: str
    user_agent: str