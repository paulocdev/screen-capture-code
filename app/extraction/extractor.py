# app/extraction/extractor.py

import re
import logging
from app.config import OCR_MIN_DIGITS

logger = logging.getLogger("ScreenReader")

def extract_numbers_from_text(raw_text: str) -> str:
    """
    Processa o texto bruto linha por linha para identificar o melhor candidato numérico.
    """
    if not raw_text:
        return ""

    lines = raw_text.splitlines()
    candidates = []

    for line in lines:
        # Remove tudo que não for dígito
        clean_digits = re.sub(r"\D", "", line)
        if len(clean_digits) >= OCR_MIN_DIGITS:
            candidates.append(clean_digits)

    if candidates:
        # Prioriza o candidato com maior extensão numérica
        best_candidate = max(candidates, key=len)
        logger.info(f"Candidato numérico encontrado ({len(best_candidate)} dígitos): {best_candidate}")
        return best_candidate

    logger.warning("Nenhum candidato numérico válido encontrado.")
    return ""