from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

from app.application.useCase.classify_email import classify_email
from app.infrastructure.providers.fileReaders.PyMuPDF.file_reader import extract_text_from_pdf

router = APIRouter()

class EmailRequest(BaseModel):
    content: str

class EmailResponse(BaseModel):
    category: str 
    confidence: float 
    suggestedResponse: str
    
class PDFExtractResponse(BaseModel):
    filename: str | None 
    text: str


@router.post("/classify", response_model=EmailResponse)
def classify(request: EmailRequest) -> EmailResponse :
    result = classify_email(request.content)
    
    print(f">>>>>>>> result \n{result}")
    
    return EmailResponse(
        category=result["category"],
        confidence=result["confidence"],
        suggestedResponse=result["suggested_response"]
    )


@router.post("/extract-pdf", response_model=PDFExtractResponse)
async def extract_pdf(file: UploadFile = File(...)) -> PDFExtractResponse:
    file_bytes = await file.read()

    text = extract_text_from_pdf(file_bytes)

    return PDFExtractResponse(
        filename=file.filename,
        text=text   
    )