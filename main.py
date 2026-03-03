from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib.hashers.bcrypt import BcryptHasher
from pwdlib import PasswordHash
import jwt
import os 
from config.db import SessionLocal, User, init_db
# main.py
from config.config import SECRET_KEY 
from config.db import get_user_by_username,get_db

# --- Config ---
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# --- Setup ---
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = PasswordHash(hashers=[BcryptHasher()])




# --- Routes ---
@app.post("/token")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
@app.get("/users/me")
def read_users_me(current_user: Annotated[dict, Depends(get_current_user)]):
    return current_user