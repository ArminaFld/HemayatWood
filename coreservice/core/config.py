from pydantic import BaseModel

class Settings(BaseModel):
    SECRET_KEY: str = "super_secret_key_change_me"
    ALGORITHM: str = "HS256"

settings = Settings()
