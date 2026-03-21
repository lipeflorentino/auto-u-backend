from src.infrastructure.adapter.ai_client import classify_with_ai
from src.infrastructure.adapter.ai_client import generate_response_with_ai
from src.infrastructure.providers.textProcessors.Spacy.nlp_processor import preprocess_text
from src.domain.entities.types import ClassificationDTO
from src.domain.dto.format import format_output

def classify_email(email_body: str) -> ClassificationDTO:
    preprocessed_content = preprocess_text(email_body)
    category, confidence = classify_with_ai(preprocessed_content)
    
    if confidence < 0.60:
        category = "PRODUTIVO" # REGRA: na duvida trata como produtivo para ter avaliação humana por causa da baixa confidence
        
    suggested_response = generate_response_with_ai(preprocessed_content, category)

    return format_output(category, confidence, suggested_response)