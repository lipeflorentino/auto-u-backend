import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PORT: int = int(os.getenv("PORT", 8080))
    HUGGINGFACE_TOKEN: str = os.getenv("HUGGINGFACE_TOKEN", "")
    CLOUD_PROVIDER: str = os.getenv("CLOUD_PROVIDER", "LOCAL") 
    STAGE: str = os.getenv("STAGE", "development")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "https://auto-u-frontend-smoky.vercel.app")
    BASE_ROUTER_URL: str = os.getenv("BASE_ROUTER_URL", "https://router.huggingface.co")
    HOST: str = os.getenv("HOST", "0.0.0.0")

settings = Settings()