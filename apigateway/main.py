from fastapi import FastAPI, Depends
from fastapi.responses import Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware
import httpx

# آدرس سرویس IAM که روی پورت 8000 اجرا می‌شود
IAM_BASE_URL = "http://127.0.0.1:8000"

app = FastAPI(title="API Gateway - Auth")

# 🔓 CORS برای توسعه (هر اوریجنی اجازه دارد)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # فعلاً همه اوریجن‌ها مجازند
    allow_credentials=False,  # چون از کوکی استفاده نمی‌کنیم، نیازی به True نیست
    allow_methods=["*"],
    allow_headers=["*"],
)

# برای اینکه Swagger دکمه Authorize را نشان بدهد
bearer_scheme = HTTPBearer()


# ---------- مدل‌های ورودی هماهنگ با IAM ----------

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserVerify(BaseModel):
    email: EmailStr
    code: str


class UserLogin(BaseModel):
    username: str
    password: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    code: str
    new_password: str


# ---------- تابع کمکی برای برگرداندن پاسخ از IAM ----------

async def proxy_response(resp: httpx.Response):
    return Response(
        content=resp.content,
        status_code=resp.status_code,
        media_type=resp.headers.get("content-type", "application/json"),
    )


@app.get("/")
async def root():
    return {"message": "API Gateway is running"}


# ---------- ثبت‌نام از طریق Gateway ----------

@app.post("/api/auth/register")
async def gateway_register(user_in: UserCreate):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{IAM_BASE_URL}/auth/register",
            json=user_in.dict(),
        )
    return await proxy_response(resp)


# ---------- تأیید کاربر از طریق Gateway ----------

@app.post("/api/auth/verify")
async def gateway_verify(data: UserVerify):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{IAM_BASE_URL}/auth/verify",
            json=data.dict(),
        )
    return await proxy_response(resp)


# ---------- لاگین از طریق Gateway (با نام کاربری) ----------

@app.post("/api/auth/login")
async def gateway_login(data: UserLogin):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{IAM_BASE_URL}/auth/login",
            json=data.dict(),
        )
    return await proxy_response(resp)


# ---------- فراموشی رمز عبور از طریق Gateway ----------

@app.post("/api/auth/forgot-password")
async def gateway_forgot_password(payload: ForgotPasswordRequest):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{IAM_BASE_URL}/auth/forgot-password",
            json=payload.dict(),
        )
    return await proxy_response(resp)


# ---------- تنظیم رمز جدید از طریق Gateway ----------

@app.post("/api/auth/reset-password")
async def gateway_reset_password(payload: ResetPasswordRequest):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{IAM_BASE_URL}/auth/reset-password",
            json=payload.dict(),
        )
    return await proxy_response(resp)


# ---------- اطلاعات کاربر فعلی از طریق Gateway ----------

@app.get("/api/auth/me")
async def gateway_me(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """
    در Swagger وقتی روی Authorize کلیک کنی و توکن را بدهی،
    هدر این‌طوری ساخته می‌شود:
        Authorization: Bearer <token>
    """
    token = credentials.credentials  # خود توکن بدون "Bearer "

    auth_header_value = f"Bearer {token}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{IAM_BASE_URL}/auth/me",
            headers={"Authorization": auth_header_value},
        )
    return await proxy_response(resp)
