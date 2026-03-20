import os
from pydantic import BaseModel
from app.infrastructure.providers.request.safe_request import safe_request
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
    
    url = f"{BASE_ROUTER_URL}/hf-inference/models/facebook/bart-large-mnli"
    
    # Opcional: Adicionar uma instrução implícita ajuda o BART a decidir melhor
    payload = {
        "inputs": content,
        "parameters": {"candidate_labels": ["PRODUTIVO", "IMPRODUTIVO"]},
        "options": {"wait_for_model": True}
    }
    
    result = safe_request(url, HEADERS, payload) 
    # result = [{'label': 'PRODUTIVO', 'score': 0.5197598934173584}, {'label': 'IMPRODUTIVO', 'score': 0.4802400767803192}]
    
    if not result or not isinstance(result, list):
        return [Classification(label="PRODUTIVO", score=0.0)]
    
    return [Classification(**item) for item in result]