from pydantic import BaseModel

class Signin(BaseModel):
    token: str
    otp: str
    user_agent: str