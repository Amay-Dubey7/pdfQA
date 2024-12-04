import pdfplumber
import tiktoken

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list:
    """Chunk text into smaller segments."""
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    chunks = []
    for i in range(0, len(tokens), chunk_size - overlap):
        chunk = tokens[i:i + chunk_size]
        chunks.append(tokenizer.decode(chunk))
    return chunks
