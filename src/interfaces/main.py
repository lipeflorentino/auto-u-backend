import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.interfaces.email_controller import router as email_router

app = FastAPI(
    title="Auto-U API",
    description="Serviço de triagem de e-mails com mDeBERTa-v3 e Llama-3",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota de Healthcheck 
@app.get("/health", tags=["Infrastructure"])
async def health_check():
    return {"status": "healthy", "provider": os.getenv("CLOUD_PROVIDER", "local")}

app.include_router(email_router)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("src.interfaces.main:app", host="0.0.0.0", port=port, reload=False)