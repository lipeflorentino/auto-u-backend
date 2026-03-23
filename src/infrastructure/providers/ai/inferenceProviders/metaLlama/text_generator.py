from src.infrastructure.providers.request.safe_request import safe_request
from src.infrastructure.env_config import settings

HEADERS = {"Authorization": f"Bearer {settings.HUGGINGFACE_TOKEN}"}

def generate_text(content: str) -> str :
    if not settings.HUGGINGFACE_TOKEN:
        print("❌ Erro: HUGGINGFACE_TOKEN não configurado no arquivo .env")
        return "Sua solicitação foi recebida e encaminhada ao setor responsável. Retornaremos em breve."
    
    # Prompt com Few-Shot (Exemplos) para forçar o formato curto e direto
    system_instruction = (
        "Você é um assistente de uma instituição financeira. "
        "Responda emails de forma curta (máximo 2 frases). "
        "Confirme o recebimento e diga que foi encaminhado ao setor responsável."
        "Exemplo 1 (Currículo): Recebemos seu currículo. Ele foi encaminhado ao nosso RH para análise.\n"
        "Exemplo 2 (Suporte): Entendemos sua dificuldade técnica. Nossa equipe de TI já está verificando o ocorrido.\n"
        "Exemplo 3 (Status): Recebemos sua solicitação de status. Vamos consultar o sistema e retornaremos em breve."
    )

    payload = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct:novita",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Email recebido: {content}"}
        ],
        "max_tokens": 1000, # Reduzido para economizar tokens
        "temperature": 0.3 # resposta mais assertiva e menos criativa
    }
    
    url = f"{settings.BASE_ROUTER_URL}/v1/chat/completions"
    
    try:
        result = safe_request(url, HEADERS, payload) 
        
        if result and "choices" in result:
            choice = result["choices"][0]
        
        # Detecta truncamento
        if choice.get("finish_reason") == "length":
            print("⚠️ Resposta truncada pelo limite de tokens")
            return None
        
        content = choice["message"]["content"].strip()

        return content
    except Exception as e:
        print(f"Erro na geração: {e}")
        
    return "Sua solicitação foi recebida e encaminhada ao setor responsável. Retornaremos em breve."