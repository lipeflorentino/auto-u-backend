from app.infrastructure.providers.ai.inferenceProviders.metaLlama.text_generator import generate_text
from app.infrastructure.providers.ai.inferenceProviders.facebookBart.text_classification import classify_text
from typing import Tuple

def classify_with_ai(content: str) -> Tuple[str, float]:
    result = classify_text(content) # [{'label': 'PRODUTIVO', 'score': 0.51}, ...]
    
    if isinstance(result, list) and len(result) > 0:
        res = result[0]
        return res.label, res.score
    return "PRODUTIVO", 0.0

def generate_response_with_ai(content: str, category: str) -> str:
    if category == "IMPRODUTIVO":
        return "Agradecemos o seu contato e desejamos um ótimo dia."

    response = generate_text(content)
    
    return response