import spacy
import re

# Carrega o modelo de linguagem natural em português
nlp = spacy.load("pt_core_news_sm")

def preprocess_email(text: str) -> str:
    text = re.sub(r'\S+@\S+', '', text) # Remove emails
    text = re.sub(r'http\S+', '', text) # Remove URLs

    doc = nlp(text.lower())
    
    # Remove Stop Words (artigos, preposições) e pontuação
    # Mantendo apenas a "Lematização" (converte palavras para a raiz: "correndo" -> "correr")
    tokens_limpos = [
        token.lemma_ for token in doc 
        if not token.is_stop and not token.is_punct and not token.is_space
    ]
    
    return " ".join(tokens_limpos)

# Exemplo:
# Entrada: "Bom dia! Gostaria de saber o status do meu processo de financiamento."
# Saída: "saber status processo financiamento"