from pydantic import BaseModel
from src.infrastructure.providers.request.safe_request import safe_request
from src.infrastructure.env_config import settings

class Classification(BaseModel):
    label: str
    score: float
    
HEADERS = {"Authorization": f"Bearer {settings.HUGGINGFACE_TOKEN}"}
    
def classify_text(content: str) -> list[Classification]:
    if not settings.HUGGINGFACE_TOKEN:
        print("❌ Erro: HUGGINGFACE_TOKEN não configurado no arquivo .env")
        return [Classification(label="PRODUTIVO", score=0.0)]
    
    url = f"{settings.BASE_ROUTER_URL}/hf-inference/models/MoritzLaurer/deberta-v3-large-zeroshot-v2.0"
    
    candidate_labels = [
        "um email produtivo que envolve solicitação, problema ou ação relacionada a serviços financeiros",
        "um email improdutivo como agradecimento, saudação, elogio ou mensagem irrelevante"
    ]
    
    payload = {
        "inputs": content,
        "parameters": {
            "candidate_labels": candidate_labels,
            "hypothesis_template": "Este email deve ser classificado como {}.", 
            "multi_label": False
        },
        "options": {"wait_for_model": True}
    }
    
    try:
        result = safe_request(url, HEADERS, payload)
        
        if result is None or not isinstance(result, list):
            print("⚠️ Erro na API ou Timeout. Retornando classificação padrão.")
            return [Classification(label="PROCESSO FINANCEIRO", score=0.0)]
        
        return [Classification(**item) for item in result]

    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return [Classification(label="PROCESSO FINANCEIRO", score=0.0)]