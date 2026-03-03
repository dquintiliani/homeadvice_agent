
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from models.login import LoginRequest,LoginResponse

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import bcrypt
from jose import jwt, ExpiredSignatureError,JWTError
from datetime import datetime, timedelta
from models.login import LoginRequest
from utils.token import is_token_valid

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

def verify_user(token: str) -> dict:
    try:
        result = is_token_valid(token)
    except Exception as e:
        print("Error during verification:", repr(e))
        return {"status": False, "msg": "Invalid Token"}

    if not result:
        return {"status": False, "msg": "Invalid Token"}

    return {"status": True, "msg": "Valid Token"}
