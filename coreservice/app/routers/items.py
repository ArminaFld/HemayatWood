from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db.session import get_db
from db.models import Item
from core.security import get_current_user

router = APIRouter(prefix="/core", tags=["core"])


class ItemCreate(BaseModel):
    title: str
    description: str | None = None


@router.get("/ping")
def ping():
    return {"message": "core pong"}


@router.get("/me")
async def me(user=Depends(get_current_user)):
    return {"user": user}


@router.post("/items")
async def create_item(
    payload: ItemCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    new_item = Item(
        title=payload.title,
        description=payload.description,
        created_by=user["id"],
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return {
        "created_by": user["id"],
        "item_id": new_item.id,
        "title": new_item.title,
        "description": new_item.description,
    }
