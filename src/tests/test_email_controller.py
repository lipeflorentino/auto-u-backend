from fastapi.testclient import TestClient
from unittest.mock import patch
from src.interfaces.main import app

client = TestClient(app)

class TestEmailController:
    """
    Suíte de testes para o controlador de e-mails.
    Simula o comportamento do Jest com organização por métodos.
    """

    @patch("src.interfaces.email_controller.classify_email")
    def test_should_classify_email_successfully(self, mock_classify):
        mock_classify.return_value = {
            "category": "PRODUTIVO",
            "confidence": 0.98,
            "suggested_response": "Obrigado pelo seu contato."
        }
        payload = {"content": "Olá, gostaria de saber sobre meu processo."}
        
        response = client.post("/classify", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "PRODUTIVO"
        assert data["confidence"] == 0.98
        assert "suggestedResponse" in data
        mock_classify.assert_called_once_with(payload["content"])

    @patch("src.interfaces.email_controller.extract_text_from_pdf")
    def test_should_extract_pdf_text_successfully(self, mock_extract):
        mock_extract.return_value = "Conteúdo extraído do PDF fictício."
        file_content = b"fake pdf content"
        files = {"file": ("test.pdf", file_content, "application/pdf")}
        
        response = client.post("/extract-pdf", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "test.pdf"
        assert "Conteúdo extraído" in data["text"]
        mock_extract.assert_called_once()

    def test_should_return_422_when_payload_is_invalid(self):
        response = client.post("/classify", json={"wrong_key": "data"})
        assert response.status_code == 422