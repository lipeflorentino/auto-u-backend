from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.interfaces.email_controller import router as email_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(email_router)