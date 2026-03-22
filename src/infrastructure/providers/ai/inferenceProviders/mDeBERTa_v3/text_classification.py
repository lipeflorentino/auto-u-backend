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
    
    url = f"{settings.BASE_ROUTER_URL}/hf-inference/models/MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"
    
    candidate_labels = [
        "SUPORTE TECNICO", 
        "PROCESSO FINANCEIRO", 
        "COMERCIAL", 
        "SPAM OU IRRELEVANTE"
    ]
    
    payload = {
        "inputs": content,
        "parameters": {
            "candidate_labels": candidate_labels,
            "hypothesis_template": "This text is an email from the finance department about {}.", # instrucao implicita para focar no contexto
            "multi_label": False
        },
        "options": {"wait_for_model": True}
    }
    
    try:
        # if settings.STAGE is "development":
        #     print("use mock!")
        #     result = [
        #         {'label': 'SUPORTE TECNICO', 'score': 0.9674391388893127},
        #         {'label': 'AGRADECIMENTO', 'score': 0.2325608015060425}
        #     ]
        # else:
        result = safe_request(url, HEADERS, payload)
        
        if result is None or not isinstance(result, list):
            print("⚠️ Erro na API ou Timeout. Retornando classificação padrão.")
            return [Classification(label="SOLICITAÇÃO FINANCEIRA", score=0.0)]
        
        return [Classification(**item) for item in result]

    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return [Classification(label="SPAM OU IRRELEVANTE", score=0.0)]