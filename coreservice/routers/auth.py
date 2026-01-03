from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx

router = APIRouter()

# مدل‌ها
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# نمونه درخواست ثبت‌نام
@router.post("/auth/register")
async def register(user_in: UserCreate):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/auth/register", json=user_in.dict()
        )
    if response.status_code != 201:
        raise HTTPException(status_code=400, detail="Registration failed")
    return response.json()

# این برای ورود به سیستم
@router.post("/auth/login")
async def login(user_in: UserCreate):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/auth/login", json=user_in.dict()
        )
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Login failed")
    return response.json()
