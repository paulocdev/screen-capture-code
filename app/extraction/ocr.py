# app/extraction/ocr.py

import pytesseract
from PIL import Image
from app.config import TESSERACT_CMD
import logging

logger = logging.getLogger("ScreenReader")

# Define o caminho do executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def run_ocr(image: Image.Image, psm: int = 6) -> str:
    """
    Executa o Tesseract OCR sobre a imagem PIL recebida.
    PSM 6 assume um bloco de texto único/uniforme.
    """
    try:
        custom_config = f"--psm {psm}"
        raw_text = pytesseract.image_to_string(image, config=custom_config)
        logger.info("OCR executado com sucesso.")
        return raw_text
    except Exception as e:
        logger.error(f"Erro ao executar Tesseract OCR: {e}")
        return ""