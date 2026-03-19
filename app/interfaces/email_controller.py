from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

from app.application.classify_email import classify_email
from app.infrastructure.FileReaders.PyMuPDF.file_reader import extract_text_from_pdf

router = APIRouter()

class EmailRequest(BaseModel):
    content: str


@router.post("/classify")
def classify(request: EmailRequest):
    result = classify_email(request.content)
    return result


@router.post("/extract-pdf")
async def extract_pdf(file: UploadFile = File(...)):
    file_bytes = await file.read()

    text = extract_text_from_pdf(file_bytes)

    return {
        "filename": file.filename,
        "text": text
    }