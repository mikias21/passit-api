from pydantic import BaseModel

class Signin(BaseModel):
    email: str
    password: str
    ip_address: str
    user_agent: str

class SigninResponseModel(BaseModel):
    access_token: str
    token_type: str