import spacy
import re

# Carregamento único do recurso pesado
_nlp = None

def get_nlp():
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("pt_core_news_sm")
        except Exception as e:
            print(f"⚠️ Aviso: Falha ao carregar Spacy ({e}). Usando limpeza básica.")
            return None
    return _nlp

def preprocess_text(text: str) -> str:
    text = re.sub(r'\S+@\S+', '', text) # Remove emails
    text = re.sub(r'http\S+', '', text) # Remove URLs

    nlp = get_nlp()
    
    # Fallback: Se o NLP não estiver disponível, retorna apenas a limpeza de Regex
    if nlp is None:
        return " ".join(text.lower().split())
    
    doc = nlp(text.lower())
    
    # Remove Stop Words (artigos, preposições) e pontuação
    # Mantendo apenas a "Lematização" (converte palavras para a raiz: "correndo" -> "correr")
    clean_tokens = [
        token.lemma_ for token in doc 
        if not token.is_stop and not token.is_punct and not token.is_space
    ]
    
    return " ".join(clean_tokens)

# Exemplo:
# Entrada: "Bom dia! Gostaria de saber o status do meu processo de financiamento."
# Saída: "saber status processo financiamento"