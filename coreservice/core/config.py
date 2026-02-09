from pydantic import BaseModel

class Settings(BaseModel):
    IAM_BASE_URL: str = "http://127.0.0.1:8000"

settings = Settings()
