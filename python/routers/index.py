from fastapi import APIRouter

router = APIRouter(prefix="")

@router.get("/")
def index():
    return {"message": "API работает!"}