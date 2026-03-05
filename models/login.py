from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"

class SignUpRequest(BaseModel):
    username: str
    password: str

class SignUpResponse(BaseModel):
    message: str