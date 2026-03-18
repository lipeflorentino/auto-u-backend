from fastapi import FastAPI
from app.interfaces.email_controller import router as email_router

app = FastAPI()

app.include_router(email_router)