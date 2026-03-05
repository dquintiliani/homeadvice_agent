
import bcrypt
import logging
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models.user import db_create_user

import bcrypt
import logging
from fastapi import HTTPException,Response,Request
from sqlalchemy.orm import Session
from models.user import db_get_user_by_username
from utils.token import create_access_token

logger = logging.getLogger(__name__)



def create_user(username: str, password: str, db: Session) -> None:
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    try:
        db_create_user(username, hashed_password, db)
    except IntegrityError:
        # SQLAlchemy raised this — username already exists
        db.rollback()
        raise HTTPException(status_code=409, detail="Username already taken")
    except Exception as e:
        # Something unexpected went wrong — log it and tell the user generically
        logger.error(f"Unexpected error during signup: {repr(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Signup failed, please try again later")

def login_user(username: str, password: str, db: Session) -> str:
    # Step 1 — does this user exist?
    user = db_get_user_by_username(username, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Step 2 — is the password correct?
    password_is_correct = bcrypt.checkpw(password.encode(), user["hashed_password"].encode())
    if not password_is_correct:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Step 3 — credentials are valid, issue a token
    token = create_access_token(user_id=user["id"], username=user["username"])

    return token
def logout_user(response: Response) -> None:
    # Step 1 — remove the token cookie from the client
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
        secure=True
    )
from utils.token import refresh_access_token

def refresh_user_token(request: Request) -> str:
    # Step 1 — extract the token from the cookie
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="No token found, please log in")

    # Step 2 — refresh the token (raises HTTPException if invalid or expired)
    new_token = refresh_access_token(token)

    return new_token
