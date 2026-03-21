import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PORT: int = int(os.getenv("PORT", 8000))
    HUGGINGFACE_TOKEN: str = os.getenv("HUGGINGFACE_TOKEN", "")
    CLOUD_PROVIDER: str = os.getenv("CLOUD_PROVIDER", "LOCAL") 

settings = Settings()