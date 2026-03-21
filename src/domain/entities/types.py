from typing import TypedDict

class ClassificationDTO(TypedDict):
    category: str
    confidence: float
    suggested_response: str

class PDFExtractionDTO(TypedDict):
    filename: str
    text: str