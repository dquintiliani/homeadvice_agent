from fastapi import APIRouter

router = APIRouter()

@router.get("/user")
def currentUser():
    return None