from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# مدل داده‌ای برای ثبت‌نام
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# مدل داده‌ای برای ورود
class UserLogin(BaseModel):
    username: str
    password: str

# API برای ثبت‌نام کاربر
@router.post("/auth/register")
async def register(user_in: UserCreate):
    # در اینجا باید اطلاعات کاربر را در دیتابیس ذخیره کنید
    # فرض کنید که کاربر به درستی ذخیره شد.
    return {"message": "User registered successfully"}

# API برای ورود کاربر
@router.post("/auth/login")
async def login(user_in: UserLogin):
    if user_in.username == "testuser" and user_in.password == "password123":
        return {"access_token": "fake-jwt-token", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

class UserVerify(BaseModel):
    email: str
    code: str

@router.post("/auth/verify")
async def verify_email(data: UserVerify):
    if data.code == "123456":
        return {"message": "Email verified successfully"}
    raise HTTPException(status_code=400, detail="Invalid verification code")
