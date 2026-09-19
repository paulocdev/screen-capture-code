# app/extraction/extractor.py

import re
import logging
from PIL import Image
from app.config import OCR_MIN_DIGITS
from app.extraction.ocr import run_ocr
from app.extraction.barcode import read_barcode
from app.extraction.preprocessing import pil_to_cv2, cv2_to_pil, rotate_image, enhance_for_ocr

logger = logging.getLogger("ScreenReader")

DANFE_KEY_LENGTH = 44

def extract_numbers_from_text(raw_text: str) -> list[str]:
    if not raw_text:
        return []

    lines = raw_text.splitlines()
    candidates = []

    for line in lines:
        clean_digits = re.sub(r"\D", "", line)
        if len(clean_digits) >= OCR_MIN_DIGITS:
            candidates.append(clean_digits)

    return candidates

def process_pipeline(image: Image.Image) -> str:
    cv_base = pil_to_cv2(image)
    all_angles = [0, 90, 180, 270]

    # 1. Tentar Código de Barras silenciosamente
    for angle in all_angles:
        rotated_cv = rotate_image(cv_base, angle)
        rotated_pil = cv2_to_pil(rotated_cv)

        barcode_result = read_barcode(rotated_pil)
        if barcode_result:
            clean_barcode = re.sub(r"\D", "", barcode_result)
            if len(clean_barcode) >= OCR_MIN_DIGITS:
                logger.info(f"✅ Código de barras detectado: {clean_barcode}")
                return clean_barcode

    # 2. OCR Silencioso com Early Exit (Interrompe no primeiro match de 44 dígitos)
    best_candidate = ""

    for angle in all_angles:
        rotated_cv = rotate_image(cv_base, angle)
        enhanced_cv = enhance_for_ocr(rotated_cv)

        # Testa na imagem tratada (3x + Sharpen) e na imagem original rotacionada
        for img_to_ocr in [cv2_to_pil(enhanced_cv), cv2_to_pil(rotated_cv)]:
            for psm in [6, 7]:
                raw_text = run_ocr(img_to_ocr, psm=psm)
                candidates = extract_numbers_from_text(raw_text)

                for candidate in candidates:
                    # Encontrou a chave completa de 44 dígitos: encerra a busca imediatamente
                    if len(candidate) == DANFE_KEY_LENGTH:
                        logger.info(f"🎯 Chave de 44 dígitos identificada com sucesso: {candidate}")
                        return candidate

                    if len(candidate) > len(best_candidate):
                        best_candidate = candidate

    if best_candidate:
        logger.info(f"🎯 Resultado extraído ({len(best_candidate)} dígitos): {best_candidate}")
        return best_candidate

    logger.warning("❌ Nenhum código numérico válido foi encontrado.")
    return ""