import os
from pydantic import BaseModel
from src.infrastructure.providers.request.safe_request import safe_request
from dotenv import load_dotenv

load_dotenv()

class Classification(BaseModel):
    label: str
    score: float
    
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
BASE_ROUTER_URL = os.getenv("BASE_ROUTER_URL")
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
    
def classify_text(content: str) -> list[Classification]:
    if not HUGGINGFACE_TOKEN:
        print("❌ Erro: HUGGINGFACE_TOKEN não configurado no arquivo .env")
        return [Classification(label="PRODUTIVO", score=0.0)]
    
    url = f"{BASE_ROUTER_URL}/hf-inference/models/MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"
    
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

    # todo: remover essa logica de desenvolvimento
    useMock = True # para testar
    
    try:
        if useMock:
            result = [
                {'label': 'SUPORTE TECNICO', 'score': 0.9674391388893127},
                {'label': 'AGRADECIMENTO', 'score': 0.2325608015060425}
            ]
        else:
            result = safe_request(url, HEADERS, payload)
        
        if result is None or not isinstance(result, list):
            print("⚠️ Erro na API ou Timeout. Retornando classificação padrão.")
            return [Classification(label="SOLICITAÇÃO FINANCEIRA", score=0.0)]
        
        return [Classification(**item) for item in result]

    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return [Classification(label="SPAM OU IRRELEVANTE", score=0.0)]