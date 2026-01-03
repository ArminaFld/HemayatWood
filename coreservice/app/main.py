from fastapi import FastAPI
from coreservice.routers import auth


app = FastAPI()

# مسیرهای مربوط به احراز هویت
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Core Service is running"}
