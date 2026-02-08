from pydantic import BaseModel


class Settings(BaseModel):
    IAM_BASE_URL: str = "http://127.0.0.1:8000"  # لوکال
    # اگر داخل docker-compose اجرا میکنی:
    # IAM_BASE_URL: str = "http://iam:8000"


settings = Settings()
