from ..entities.types import ClassificationDTO

def format_output(category: str, confidence: float, response_text: str) -> ClassificationDTO:
    return {
        "category": category,
        "confidence": confidence,
        "suggested_response": response_text
    }