from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

from app.application.classify_email import classify_email
from app.infrastructure.services.FileReaders.PyMuPDF.file_reader import extract_text_from_pdf
from app.infrastructure.services.TextProcessors.Spacy import preprocess_email

router = APIRouter()

class EmailRequest(BaseModel):
    content: str


@router.post("/classify")
def classify(request: EmailRequest):
    preprocessed_content = preprocess_email(request.content)
    result = classify_email(preprocessed_content)
    return result


@router.post("/extract-pdf")
async def extract_pdf(file: UploadFile = File(...)):
    file_bytes = await file.read()

    text = extract_text_from_pdf(file_bytes)

    return {
        "filename": file.filename,
        "text": text
    }