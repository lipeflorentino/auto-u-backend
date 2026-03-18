def classify_with_ai(content: str) -> str:
    # MOCK inicial
    if "obrigado" in content.lower():
        return "IMPRODUTIVO"
    return "PRODUTIVO"


def generate_response(content: str, category: str) -> str:
    if category == "PRODUTIVO":
        return "Recebemos sua solicitação e retornaremos em breve."
    return "Agradecemos sua mensagem."