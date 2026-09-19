# app/extraction/ocr.py

import pytesseract
from PIL import Image
from app.config import TESSERACT_CMD
import logging

logger = logging.getLogger("ScreenReader")

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def run_ocr(image: Image.Image, psm: int = 6) -> str:
    """
    Executa o Tesseract OCR restringindo a leitura estritamente a números.
    """
    try:
        # Configuração restrita apenas para caracteres numéricos (0-9)
        custom_config = f"--psm {psm} -c tessedit_char_whitelist=0123456789"
        raw_text = pytesseract.image_to_string(image, config=custom_config)
        return raw_text
    except Exception as e:
        logger.error(f"Erro ao executar Tesseract OCR: {e}")
        return ""