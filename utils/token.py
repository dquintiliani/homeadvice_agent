# ─────────────────────────────────────────
# utils/token.py
# Job: create, validate, and refresh JWT tokens
# ─────────────────────────────────────────
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
import os
from typing import cast

# ── Configuration ────────────────────────
# Fail loudly if SECRET_KEY is missing — never fall back to a weak default
from dotenv import load_dotenv

# Load environment variables from .env.local before reading them
load_dotenv(".env.local")

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is not set")
SECRET_KEY = cast(str, SECRET_KEY)  # tells Pylance: trust me, this is a str

ALGORITHM          = os.getenv("JWT_ALGORITHM", "HS256")
EXPIRE_MINUTES     = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
ALLOWED_CLAIMS     = {"sub", "email", "role"}


# ── Token Creation ───────────────────────
def create_access_token(user_id: int, username: str) -> str:
    # Explicit arguments instead of a raw dict — caller can't pass unexpected claims
    payload = {
        "sub":   str(user_id),
        "email": username,
        "exp":   datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM) # pyright: ignore[reportArgumentType]


# ── Token Validation ─────────────────────
def decode_token(token: str) -> dict:
    # Returns the payload on success, raises HTTPException on failure
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # pyright: ignore[reportArgumentType]
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ── Token Refresh ────────────────────────
def refresh_access_token(token: str) -> str:
    # Decode the old token — raises HTTPException if invalid
    payload = decode_token(token)

    # Strip time-based claims so create_access_token sets fresh ones
    user_id  = payload.get("sub")
    username = payload.get("email")

    if not user_id or not username:
        raise HTTPException(status_code=401, detail="Token is missing required claims")

    return create_access_token(user_id=int(user_id), username=username)