from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterResponse(BaseModel):
    email: EmailStr
    totp_secret: str
    otpauth_uri: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TempTokenResponse(BaseModel):
    temp_token: str
    message: str = "Password verified. Please provide your TOTP code."
