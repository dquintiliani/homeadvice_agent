
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from models.login import LoginRequest,LoginResponse

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from models.login import LoginRequest

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
            text("SELECT id,username, password_hash FROM users WHERE username = :username"),
            {"username": username},
        ).fetchone()
    except Exception:
        # DB error, not user error
        return (False, "Login failed",None)

    # Normal flow: no exception, now validate credentials
    if not result:
        return (False, "Invalid username or password",None)

    db_username, password_hash = result

    if not bcrypt.checkpw(password.encode(), password_hash.encode()):
        return (False, "Invalid username or password",None)

    return (True, "Login successful",result.id)

def create_user(username: str, password: str, db):
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    try:    
        db.execute(
            text("INSERT INTO users (username, password_hash) VALUES (:username, :password_hash)"),
            {"username": username, "password_hash": password_hash}
        )
    except Exception:
        return (False, "Signup Failed")
    return (True, "Signup successful")