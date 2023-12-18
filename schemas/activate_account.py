from pydantic import BaseModel

class ActivateAccountResponseModel(BaseModel):
    message: str
    status: int