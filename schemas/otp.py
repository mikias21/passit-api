from pydantic import BaseModel

class OTP(BaseModel):
    otp: str