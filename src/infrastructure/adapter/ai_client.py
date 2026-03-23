from src.infrastructure.providers.ai.inferenceProviders.metaLlama.text_generator import generate_text
from src.infrastructure.providers.ai.inferenceProviders.mDeBERTa_v3.text_classification import classify_text
from typing import Tuple

def classify_with_ai(content: str) -> Tuple[str, float]:
    results = classify_text(content)

    if not results or len(results) == 0:
        return "PRODUTIVO", 0.0

    top = results[0]

    label = top.label.lower()
    score = top.score
    
    if "improdutivo" in label:
        final_category = "IMPRODUTIVO"
    else:
        final_category = "PRODUTIVO"

    threshold = 0.60

    if score < threshold:
        print(f"⚠️ Confiança Baixa ({score:.4f}).")
        return "PRODUTIVO", score

    print(f"✅ Decisão Final: {final_category} | Score: {score:.4f}")

    return final_category, score

def generate_response_with_ai(content: str, category: str) -> str:
    if category == "IMPRODUTIVO":
        return "Agradecemos o seu contato e desejamos um ótimo dia."

    response = generate_text(content)
    
    if not response:
        return (
            "Recebemos sua mensagem e ela foi encaminhada ao setor responsável. "
            "Retornaremos em breve."
        )
    
    return response