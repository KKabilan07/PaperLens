from fastapi import APIRouter

router = APIRouter()

@router.get("/me")
def get_user():
    return {"user": "mock user"}