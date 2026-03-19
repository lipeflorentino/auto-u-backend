from app.infrastructure.services.AI.ai_client import classify_with_ai
from app.infrastructure.services.AI.ai_client import generate_response

def classify_email(content: str):
    category = classify_with_ai(content)
    response = generate_response(content, category)

    return {
        "category": category,
        "suggested_response": response
    }