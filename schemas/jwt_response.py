from pydantic import BaseModel

class JWTResponseModel(BaseModel):
    message: str
    status: int