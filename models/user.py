from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Boolean,text
from sqlalchemy.ext.declarative import declarative_base

from models.login import LoginRequest,LoginResponse

from fastapi import HTTPException,Response
import bcrypt
from jose import jwt, ExpiredSignatureError,JWTError
from datetime import datetime, timedelta
from models.login import LoginRequest


from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends


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


def db_create_user(username: str, hashed_password: str, db: Session) -> None:
    # Just execute the SQL — SQLAlchemy raises errors if anything goes wrong
    db.execute(
        text("INSERT INTO users (username, hashed_password) VALUES (:username, :hashed_password)"),
        {"username": username, "hashed_password": hashed_password}
    )
    db.commit()



def db_get_user_by_username(username: str, db: Session) -> dict | None:
    result = db.execute(
        text("SELECT id, username, hashed_password FROM users WHERE username = :username"),
        {"username": username}
    ).fetchone()

    # Return None if user doesn't exist — let the controller decide what that means
    if not result:
        return None

    return {
        "id": result.id,
        "username": result.username,
        "hashed_password": result.hashed_password
    }


