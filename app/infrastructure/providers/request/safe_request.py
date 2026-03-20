import requests

def safe_request(url, headers, payload):
    try:
        response = requests.post(
            url, 
            headers=headers, 
            json={**payload},
            timeout=30
        )
        
        if response.status_code == 200:
            print(response.json())
            return response.json()
        
        print(f"Erro API ({response.status_code}): {response.text}")
        return None
    except requests.exceptions.JSONDecodeError:
        print("Erro: A API não retornou um JSON válido.")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None