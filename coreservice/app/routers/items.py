from fastapi import APIRouter, Depends
from pydantic import BaseModel

from core.security import get_current_user

router = APIRouter(prefix="/core", tags=["core"])

class ItemCreate(BaseModel):
    title: str
    description: str | None = None

@router.get("/ping")
def ping():
    return {"message": "core pong"}

@router.get("/me")
def me(user=Depends(get_current_user)):
    # payload توکن رو برمی‌گردونه (فعلا)
    return {"user": user}

@router.post("/items")
def create_item(payload: ItemCreate, user=Depends(get_current_user)):
    # فعلا فقط نمونه
    return {"created_by": user.get("sub"), "item": payload}
