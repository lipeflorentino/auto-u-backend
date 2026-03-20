import fitz  # PyMuPDF

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text_content = []

    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text = page.get_text("text")
            text_content.append(text)

    return "\n".join(text_content).strip()