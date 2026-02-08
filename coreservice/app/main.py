from fastapi import FastAPI
from app.routers import auth
from app.routers import items

app = FastAPI(title="Core Service")

app.include_router(auth.router)
app.include_router(items.router)

@app.get("/")
def root():
    return {"message": "Core Service is running"}
