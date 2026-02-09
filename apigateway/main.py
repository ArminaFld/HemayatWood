from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.responses import Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from typing import Any, Dict

IAM_BASE_URL = os.getenv("IAM_BASE_URL", "http://127.0.0.1:8000")
MEDIA_SERVICE_URL = os.getenv("MEDIA_SERVICE_URL", "http://127.0.0.1:8003")
CORE_SERVICE_URL = os.getenv("CORE_SERVICE_URL", "http://127.0.0.1:8001")

app = FastAPI(title="API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

bearer_scheme = HTTPBearer()


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


async def proxy_response(resp: httpx.Response):
    return Response(
        content=resp.content,
        status_code=resp.status_code,
        media_type=resp.headers.get("content-type", "application/json"),
    )


@app.get("/")
async def root():
    return {"message": "API Gateway is running"}


@app.post("/api/auth/register")
async def gateway_register(user_in: UserCreate):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{IAM_BASE_URL}/auth/register",
            json=user_in.model_dump(),
        )
    return await proxy_response(resp)


@app.post("/api/auth/verify")
async def gateway_verify(data: UserVerify):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{IAM_BASE_URL}/auth/verify",
            json=data.model_dump(),
        )
    return await proxy_response(resp)


@app.post("/api/auth/login")
async def gateway_login(data: UserLogin):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{IAM_BASE_URL}/auth/login",
            json=data.model_dump(),
        )
    return await proxy_response(resp)


@app.post("/api/auth/forgot-password")
async def gateway_forgot_password(payload: ForgotPasswordRequest):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{IAM_BASE_URL}/auth/forgot-password",
            json=payload.model_dump(),
        )
    return await proxy_response(resp)


@app.post("/api/auth/reset-password")
async def gateway_reset_password(payload: ResetPasswordRequest):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{IAM_BASE_URL}/auth/reset-password",
            json=payload.model_dump(),
        )
    return await proxy_response(resp)


@app.get("/api/auth/me")
async def gateway_me(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{IAM_BASE_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
    return await proxy_response(resp)

@app.post("/api/media/upload/")
async def gateway_upload_file(file: UploadFile = File(...)):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{MEDIA_SERVICE_URL}/upload/",
            files={"file": (file.filename, file.file, file.content_type)},
        )

    if resp.status_code == 200:
        return resp.json()
    raise HTTPException(status_code=resp.status_code, detail="File upload failed")


@app.get("/api/media/files/{filename}")
async def gateway_get_file(filename: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{MEDIA_SERVICE_URL}/files/{filename}")

    if resp.status_code == 200:
        return resp.json()
    raise HTTPException(status_code=resp.status_code, detail="File not found")


@app.delete("/api/media/files/{filename}")
async def gateway_delete_file(filename: str):
    async with httpx.AsyncClient() as client:
        resp = await client.delete(f"{MEDIA_SERVICE_URL}/files/{filename}")

    if resp.status_code == 200:
        return resp.json()
    raise HTTPException(status_code=resp.status_code, detail="File not found")

@app.get("/api/core/ping")
async def gateway_core_ping():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{CORE_SERVICE_URL}/core/ping")
    return await proxy_response(resp)


@app.get("/api/core/me")
async def gateway_core_me(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{CORE_SERVICE_URL}/core/me",
            headers={"Authorization": f"Bearer {token}"},
        )
    return await proxy_response(resp)


@app.post("/api/core/items")
async def gateway_core_create_item(
    payload: Dict[str, Any],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    token = credentials.credentials
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{CORE_SERVICE_URL}/core/items",
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
        )
    return await proxy_response(resp)
