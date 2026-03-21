import time
from src.infrastructure.adapter.ai_client import CLASSIFIER_URL, GENERATOR_URL
from src.infrastructure.providers.request.safe_request import safe_request

def wakeup_models():
    print("--- Iniciando Warm-up dos Modelos ---")
    
    models = {
        "Classificador (BART)": CLASSIFIER_URL,
        "Gerador (Meta Llama)": GENERATOR_URL
    }

    for name, url in models.items():
        print(f"Acordando {name}...")
        attempts = 0
        success = False
        
        while attempts < 3 and not success:
            res = safe_request(url, {"inputs": "warmup"})
            if res:
                print(f"[OK] {name} está pronto!")
                success = True
            else:
                attempts += 1
                print(f"[...] {name} ainda carregando... Tentativa {attempts}/3")
                time.sleep(5) # Espera 5 segundos para o servidor subir o modelo
                
    print("--- Warm-up Finalizado ---\n")

if __name__ == "__main__":
    wakeup_models()