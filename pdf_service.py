from pathlib import Path
from typing import Optional
import io
import fitz  # requires: pip install pymupdf

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    given raw bytes of a pdf file
    return the full extracted text content
    uses pymupdf for high fidelity extraction
    """
    try:
        # open pdf from memory stream
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        # log error in production
        return ""

def extract_text_from_file(file_path: Path) -> str:
    """
    given a path to a local pdf file
    return the extracted text content
    """
    if not file_path.exists():
        return ""
    
    try:
        with fitz.open(file_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        return ""
