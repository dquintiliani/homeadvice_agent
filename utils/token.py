import bcrypt
from jose import jwt, JWTError,ExpiredSignatureError
from datetime import datetime, timedelta,timezone
import os
from dotenv import load_dotenv
now_utc = datetime.now(timezone.utc)

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",30))
SECRET_KEY = os.getenv("SECRET_KEY",'123')
ALGORITHM = os.getenv("JWT_ALGORITHM",'HS256')

def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def refresh_token(token: str) -> str:   
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise ValueError("Invalid or expired token")
    # Remove old exp/iat/nbf if present
    for claim in ("exp", "iat", "nbf"):
        payload.pop(claim, None)

    # Issue a new token with the same payload but new expiry
    new_token = create_token(payload)
    return new_token

def is_token_valid(token: str) -> bool:
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except ExpiredSignatureError:
        # token is expired
        return False
    except JWTError:
        # token is invalid for some other reason
        return False
    
