from fastapi import APIRouter
from pydantic import BaseModel
from app.application.classify_email import classify_email

router = APIRouter()

class EmailRequest(BaseModel):
    content: str

@router.post("/classify")
def classify(request: EmailRequest):
    result = classify_email(request.content)
    return result