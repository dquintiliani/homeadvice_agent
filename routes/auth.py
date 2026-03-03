from models.login import LoginRequest,LoginResponse
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from models.user import login_user,create_user
from utils.token import create_token
from config.db import get_db

router = APIRouter()
# /login Post Request 


@router.post("/login",response_model=LoginResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db),) -> LoginResponse:
    ok, msg, user_id = login_user(credentials.username, credentials.password, db)
    if not ok:
        # tell FastAPI to send a proper error response
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=msg,
        )
    token = create_token({"user":credentials.username,"role":"basic","uid":user_id})
    
    return LoginResponse(
        access_token=token,
        token_type="bearer",
    )

@router.post("/signup",response_model=LoginResponse)
def signup(credentials: LoginRequest,db: Session = Depends(get_db),):
    res,msg = create_user(credentials.username,credentials.password, db)
    if not res:
        return res,msg
    
    return res,msg

@router.post("/refresh",response_model=LoginResponse)
def refreshUser(credentials: LoginRequest,db: Session = Depends(get_db),):
    res,msg = create_user(credentials.username,credentials.password, db)
    if not res:
        return res,msg
    
    return res,msg


