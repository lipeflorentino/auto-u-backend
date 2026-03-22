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
        "Sua tarefa é ler um email e gerar uma resposta curta (máximo 2 frases). "
        "A resposta deve: 1. Confirmar que entendeu o assunto. 2. Indicar que foi encaminhado ao setor responsável.\n\n"
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
        "max_tokens": 60, # Reduzido para economizar tokens
        "temperature": 0.3 # resposta mais assertiva e menos criativa
    }
    
    url = f"{settings.BASE_ROUTER_URL}/v1/chat/completions"
    
    try:
        if settings.STAGE is "development":
            print("use mock!")
            result = {'id': '486f8d7d521d485fab5549c7c9a8db20', 'object': 'chat.completion', 'created': 1773969828, 'model': 'meta-llama/llama-3-8b-instruct', 'choices': [{'index': 0, 'message': {'role': 'assistant', 'content': 'Obrigada pelo contato, tenha um otimo dia.'}, 'finish_reason': 'stop'}], 'usage': {'prompt_tokens': 785, 'completion_tokens': 26, 'total_tokens': 811, 'prompt_tokens_details': None, 'completion_tokens_details': None}, 'system_fingerprint': ''}
        else:
            result = safe_request(url, HEADERS, payload) 
        
        if result and "choices" in result:
            return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Erro na geração: {e}")
        
    return "Sua solicitação foi recebida e encaminhada ao setor responsável. Retornaremos em breve."