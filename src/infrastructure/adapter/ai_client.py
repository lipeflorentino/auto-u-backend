from src.infrastructure.providers.ai.inferenceProviders.metaLlama.text_generator import generate_text
from src.infrastructure.providers.ai.inferenceProviders.mDeBERTa_v3.text_classification import classify_text
from typing import Tuple

def classify_with_ai(content: str) -> Tuple[str, float]:
    results = classify_text(content)
    
    if not results or len(results) == 0:
        return "PRODUTIVO", 0.0
        
    mappings = {
        "suporte tecnico": "PRODUTIVO", 
        "processo financeiro": "PRODUTIVO", 
        "agradecimento": "IMPRODUTIVO", 
        "spam": "IMPRODUTIVO",
        "saudação": "IMPRODUTIVO"
    }
    
    category_scores = {"PRODUTIVO": 0.0, "IMPRODUTIVO": 0.0}
   
    for res in results:
        category = mappings.get(res.label, "IMPRODUTIVO")
        category_scores[category] += res.score
        print(f"📊 Parcial IA: Label='{res.label}' | Score={res.score:.4f} -> Categoria: {category}")
        
    final_category = max(category_scores, key=category_scores.get)
    final_score = category_scores[final_category]
    
    threshold = 0.60 
    
    if final_score < threshold:
        print(f"⚠️ Confiança Baixa ({final_score:.4f}).")
        return "PRODUTIVO", final_score

    print(f"✅ Decisão Final: {final_category} | Confiança Somada: {final_score:.4f}")
    return final_category, final_score

def generate_response_with_ai(content: str, category: str) -> str:
    if category == "IMPRODUTIVO":
        return "Agradecemos o seu contato e desejamos um ótimo dia."

    response = generate_text(content)
    
    return response