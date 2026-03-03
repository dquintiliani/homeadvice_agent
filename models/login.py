from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str
    
class LoginResponse(BaseModel):
    responseStatus: bool
    access_token: str | None
    token_type: str = "bearer" 
 



