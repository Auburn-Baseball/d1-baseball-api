from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "D1 Baseball API built by Auburn University!"}

@router.get("/conferences/{year}")
async def read_item(year: int):
    return {}