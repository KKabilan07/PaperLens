from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def ask_question():
    return {"answer": "This will be AI response later"}