
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from utils.token import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/users/login")

def auth_required(token: str = Depends(oauth2_scheme)):
    # decode_token raises a 401 HTTPException automatically if the token is invalid
    decode_token(token)