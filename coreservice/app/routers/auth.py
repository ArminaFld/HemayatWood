from fastapi import APIRouter, Depends
from core.security import get_current_user


router = APIRouter(
    prefix="/core",
    tags=["core"],
)


@router.get("/health")
async def health():
    return {"status": "Core service alive"}


@router.get("/profile")
async def profile(user=Depends(get_current_user)):
    """
    فقط کاربر لاگین شده می‌تونه اینو ببینه
    توکن توسط IAM validate میشه
    """
    return {
        "message": "authorized",
        "user": user,
    }
