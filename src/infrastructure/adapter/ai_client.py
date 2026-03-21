from src.infrastructure.providers.ai.inferenceProviders.metaLlama.text_generator import generate_text
from src.infrastructure.providers.ai.inferenceProviders.mDeBERTa_v3.text_classification import classify_text
from typing import Tuple

def classify_with_ai(content: str) -> Tuple[str, float]:
    results = classify_text(content)
    
    if not results or len(results) == 0:
        return "PRODUTIVO", 0.0

    best_result = results[0]
    label = best_result.label
    score = best_result.score
    
    print(f"🔍 IA Original: Label='{best_result.label}' | Score={best_result.score:.4f}")
        
    mappings = {
        "SUPORTE TECNICO": "PRODUTIVO", 
        "PROCESSO FINANCEIRO": "PRODUTIVO", 
        "COMERCIAL": "PRODUTIVO", 
        "SPAM OU IRRELEVANTE": "IMPRODUTIVO",
        "IMPRODUTIVO": "IMPRODUTIVO"
    }
    
    final_category = mappings.get(label)

    if final_category is None:
        print(f"⚠️ Label '{best_result.label}' não mapeada. Usando fallback PRODUTIVO.")
        return "PRODUTIVO", 0.0
    
    return final_category, score

def generate_response_with_ai(content: str, category: str) -> str:
    if category == "IMPRODUTIVO":
        return "Agradecemos o seu contato e desejamos um ótimo dia."

    response = generate_text(content)
    
    return response