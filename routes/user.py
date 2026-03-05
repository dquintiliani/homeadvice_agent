from fastapi import APIRouter, Depends, Response,Request
from sqlalchemy.orm import Session
from controllers.user import create_user,login_user,logout_user,refresh_user_token
from config.db import get_db          # your DB session dependency
from models.login import SignUpRequest,LoginRequest

router = APIRouter(prefix="/users")

@router.post("/signup", status_code=201)
def signup(request: SignUpRequest, db: Session = Depends(get_db)):
    create_user(request.username, request.password, db)
    return {"message": "Account created successfully"}


@router.post("/login", status_code=200)
def login(request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    token = login_user(request.username, request.password, db)

    # Set the token as a secure cookie so the browser holds it automatically
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,   # JavaScript cannot read this cookie
        samesite="lax",  # protects against cross-site request forgery
        secure=True      # only sent over HTTPS
    )
    
    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }
    
@router.post("/logout", status_code=200)
def logout(response: Response):
    # Step 1 — call the controller to delete the token cookie
    logout_user(response)

    # Step 2 — confirm to the client that logout was successful
    return {"message": "Logout successful"}

@router.post("/refresh", status_code=200)
def refresh(request: Request, response: Response):
    # Step 1 — call the controller to get a fresh token
    new_token = refresh_user_token(request)

    # Step 2 — set the new token as a cookie
    response.set_cookie(
        key="access_token",
        value=new_token,
        httponly=True,
        samesite="lax",
        secure=True
    )

    # Step 3 — return the new token in the body for Swagger
    return {
        "message":      "Token refreshed successfully",
        "access_token": new_token,
        "token_type":   "bearer"
    }
    

from dependencies.auth import auth_required

@router.get("/protected", status_code=200, dependencies=[Depends(auth_required)])
def protected_route():
    # FastAPI runs auth_required before this function is called
    # If the token is invalid, auth_required raises a 401 — we never get here
    return {"message": "You are authenticated"}