from fastapi import APIRouter

home_router = APIRouter()

@home_router.get("/")
async def root():
    return {"message": "Welcome to the API!"}