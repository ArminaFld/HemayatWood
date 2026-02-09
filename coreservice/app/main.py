from fastapi import FastAPI
from app.routers import auth, items
from db.base import Base
from db.session import engine
import db.models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Core Service")

app.include_router(auth.router)
app.include_router(items.router)

@app.get("/")
def root():
    return {"message": "Core Service is running"}
