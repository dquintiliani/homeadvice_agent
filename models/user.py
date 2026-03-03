
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from models.login import LoginRequest,LoginResponse

from fastapi import HTTPException,Response
from sqlalchemy.orm import Session
from sqlalchemy import text
import bcrypt
from jose import jwt, ExpiredSignatureError,JWTError
from datetime import datetime, timedelta
from models.login import LoginRequest
from utils.token import is_token_valid

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Create the Base class if not already defined elsewhere
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
    usertype = Column(String,default="Basic")


def login_user(username: str, password: str, db: Session) -> tuple[bool, str,int|None]:
    try:
        result = db.execute(
            text("SELECT id, username, hashed_password FROM users WHERE username = :username"),
            {"username": username},
        ).fetchone()
    except Exception as e:
        print(f"DB error during login: {e}")
        return (False, "Login failed", None)

    # Normal flow: no exception, now validate credentials
    if not result:
        return (False, "Invalid username or password",None)
    user_id, db_username, password_hash = result  

    if not bcrypt.checkpw(password.encode(), password_hash.encode()):
        return (False, "Invalid username or password",None)

    return (True, "Login successful",result.id)

def logout_user(response: Response) -> tuple[bool, str]:
    try:
        response.delete_cookie(
            key="access_token",
            httponly=True,
            samesite="lax",
            secure=True
        )
        return (True, "Logged out successfully")
    except Exception as e:
        print(f"Logout error: {e}")
        return (False, "Logout failed")

def create_user(username: str, password: str, db):
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print("create_user got db:", db, type(db))  # debug
    try:    
        db.execute(
            text("INSERT INTO users (username, hashed_password) VALUES (:username, :password_hash)"),
            {"username": username, "password_hash": password_hash}
        )
        db.commit()
    except Exception as e:
        print("Error during create_user:", repr(e))  # <-- THIS is key
        return (False, "Signup Failed")
    return (True, "Signup successful")

def verify_user(token: str) -> tuple[bool, str]:
    try:
        result = is_token_valid(token)
    except Exception as e:
        return (False, f"Error during verification: {repr(e)}")
    if not result:
        return (False, "Token verification unsuccessful")
    return (True, "Token verification successful")
# dependencies/auth.py — FastAPI dependency for guarding routes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def auth_required(token: str = Depends(oauth2_scheme)):
    ok, msg = verify_user(token)
    if not ok:
        raise HTTPException(status_code=401, detail=msg)


def get_user(username: str, db: Session) -> tuple[bool, str, dict | None]:
    try:
        result = db.execute(
            text("SELECT id, username, hashed_password FROM users WHERE username = :username"),
            {"username": username}
        ).fetchone()
    except Exception as e:
        print(f"DB error in get_user: {e}")
        return (False, "Database error", None)

    if not result:
        return (False, "User not found", None)
    return (True, "User found", {
        "id": result.id,
        "username": result.username,
        "hashed_password": result.hashed_password
    })
