from pydantic import BaseModel

class Signin(BaseModel):
    email: str
    password: str
    ip_address: str
    user_agent: str