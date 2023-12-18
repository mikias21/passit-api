from pydantic import BaseModel

class Signup(BaseModel):
    is_email: bool | None
    is_phone: bool | None
    email: str
    password: str
    ip_address: str
    user_agent: str

class SignupResponseModel(BaseModel):
    message: str
    status: int