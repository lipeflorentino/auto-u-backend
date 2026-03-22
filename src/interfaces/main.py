import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.env_config import settings

from src.interfaces.email_controller import router as email_router

app = FastAPI(
    title="Auto-U API",
    description="Serviço de triagem de e-mails com mDeBERTa-v3 e Llama-3",
    version="1.0.0"
)

origins = [
    settings.FRONTEND_URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Rota de Healthcheck 
@app.get("/health", tags=["Infrastructure"])
async def health_check():
    return {"status": "healthy", "provider": settings.CLOUD_PROVIDER}

app.include_router(email_router)

if __name__ == "__main__":
    port = int(settings.PORT)
    host = settings.HOST
    uvicorn.run("src.interfaces.main:app", host=host, port=port, reload=False)