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

def get_smart_angle_order(width: int, height: int) -> list[int]:
    """
    Se a seleção for mais alta que larga (vertical), testa 270° e 90° primeiro.
    Se for mais larga que alta (horizontal), testa 0° e 180° primeiro.
    """
    if height > width:
        return [270, 90, 0, 180]
    return [0, 180, 270, 90]

def process_pipeline(image: Image.Image) -> str:
    cv_base = pil_to_cv2(image)
    height, width = cv_base.shape[:2]
    ordered_angles = get_smart_angle_order(width, height)

    # 1. Leitura direta via Código de Barras (Ultra-rápido)
    for angle in ordered_angles:
        rotated_cv = rotate_image(cv_base, angle)
        rotated_pil = cv2_to_pil(rotated_cv)

        barcode_result = read_barcode(rotated_pil)
        if barcode_result:
            clean_barcode = re.sub(r"\D", "", barcode_result)
            if len(clean_barcode) >= OCR_MIN_DIGITS:
                logger.info(f"✅ Código de barras detectado ({angle}°): {clean_barcode}")
                return clean_barcode

    # 2. Passagem Rápida (OCR na imagem tratada com a rotação mais provável)
    best_candidate = ""

    for angle in ordered_angles:
        rotated_cv = rotate_image(cv_base, angle)
        enhanced_cv = enhance_for_ocr(rotated_cv)
        enhanced_pil = cv2_to_pil(enhanced_cv)

        # PSM 6: Bloco de texto / linha única
        raw_text = run_ocr(enhanced_pil, psm=6)
        candidates = extract_numbers_from_text(raw_text)

        for candidate in candidates:
            if len(candidate) == DANFE_KEY_LENGTH:
                logger.info(f"🎯 Chave de 44 dígitos identificada ({angle}°): {candidate}")
                return candidate

            if len(candidate) > len(best_candidate):
                best_candidate = candidate

    # 3. Fallback (Apenas se a passagem rápida não encontrou os 44 dígitos)
    if not best_candidate or len(best_candidate) < DANFE_KEY_LENGTH:
        for angle in ordered_angles:
            rotated_cv = rotate_image(cv_base, angle)
            raw_text = run_ocr(cv2_to_pil(rotated_cv), psm=7)
            candidates = extract_numbers_from_text(raw_text)

            for candidate in candidates:
                if len(candidate) == DANFE_KEY_LENGTH:
                    logger.info(f"🎯 Chave identificada via Fallback ({angle}°): {candidate}")
                    return candidate
                if len(candidate) > len(best_candidate):
                    best_candidate = candidate

    if best_candidate:
        logger.info(f"🎯 Resultado extraído ({len(best_candidate)} dígitos): {best_candidate}")
        return best_candidate

    logger.warning("❌ Nenhum código numérico válido foi encontrado.")
    return ""