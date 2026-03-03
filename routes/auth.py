from models.login import LoginRequest,LoginResponse
from fastapi import APIRouter,Depends,HTTPException,status,Response
from sqlalchemy.orm import Session
from models.user import login_user,create_user,logout_user,get_user,verify_user
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
    token = create_token(
    {"user": credentials.username, 
     "role": "basic", 
     "uid": user_id}
    )
    return LoginResponse(
        responseStatus=True,
        access_token=token,
        token_type="bearer",
    )
    
@router.post("/logout")
def logout(response: Response):
    ok, msg = logout_user(response)
    if not ok:
        raise HTTPException(status_code=500, detail=msg)
    return {"message": msg}


@router.post("/signup",response_model=LoginResponse)
def signup(credentials: LoginRequest,db: Session = Depends(get_db),):
    res,msg = create_user(credentials.username,credentials.password, db)
    if not res:
        print(msg)
        return LoginResponse(
        responseStatus=False,
        access_token=None,
        token_type="bearer",
    )
    print(msg)
    return LoginResponse(
        responseStatus=True,
        access_token=None,
        token_type="bearer",
    )

@router.post("/refresh",response_model=LoginResponse)
def refreshUser(credentials: LoginRequest,db: Session = Depends(get_db),):
    res,msg = create_user(credentials.username,credentials.password, db)
    if not res:
        return res,msg
    return res,msg

@router.get("/{username}", dependencies=[Depends(verify_user)])
def find_user_route(username: str, db: Session = Depends(get_db)):
    ok, msg, data = get_user(username, db)
    if not ok:
        raise HTTPException(status_code=404, detail=msg)
    return data


