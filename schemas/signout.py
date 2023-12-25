from pydantic import BaseModel

class SignoutModel(BaseModel):
    message: str
    status: int