# app/extraction/extractor.py

import re
import logging
from PIL import Image
from app.config import OCR_MIN_DIGITS
from app.extraction.ocr import run_ocr
from app.extraction.barcode import read_barcode
from app.extraction.preprocessing import pil_to_cv2, cv2_to_pil, rotate_image, preprocess_image

logger = logging.getLogger("ScreenReader")

def extract_numbers_from_text(raw_text: str) -> list[str]:
    """Retorna uma lista de todas as sequências numéricas válidas da leitura."""
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
    """
    Pipeline completo:
    1. Testa Barcode em todos os ângulos.
    2. Se não encontrar, roda OCR em TODOS os ângulos (0°, 90°, 180°, 270°) e coleta todos os candidatos.
    3. Seleciona a sequência numérica mais longa (ex: a chave de 44 dígitos).
    """
    cv_base = pil_to_cv2(image)
    all_angles = [0, 90, 180, 270]

    # 1. Tentar leitura direta de Código de Barras em todos os ângulos
    for angle in all_angles:
        rotated_cv = rotate_image(cv_base, angle)
        rotated_pil = cv2_to_pil(rotated_cv)

        barcode_result = read_barcode(rotated_pil)
        if barcode_result:
            clean_barcode = re.sub(r"\D", "", barcode_result)
            if len(clean_barcode) >= OCR_MIN_DIGITS:
                logger.info(f"✅ Código de barras detectado ({angle}°): {clean_barcode}")
                return clean_barcode

    # 2. Se não encontrou código de barras, executa OCR em todos os ângulos
    ocr_candidates = []

    for angle in all_angles:
        logger.info(f"Analisando OCR no ângulo {angle}°...")
        rotated_cv = rotate_image(cv_base, angle)
        processed_cv = preprocess_image(rotated_cv)

        # Testa tanto na imagem pré-processada quanto na rotacionada original
        for img_to_ocr in [cv2_to_pil(processed_cv), cv2_to_pil(rotated_cv)]:
            # Testa PSM 6 (bloco de texto) e PSM 7 (linha única)
            for psm in [6, 7]:
                raw_text = run_ocr(img_to_ocr, psm=psm)
                candidates = extract_numbers_from_text(raw_text)
                for candidate in candidates:
                    logger.info(f"  └─ Candidato ({angle}°, PSM {psm}): {candidate} [{len(candidate)} dígitos]")
                    ocr_candidates.append(candidate)

    if ocr_candidates:
        # Escolhe a maior sequência numérica encontrada
        best_candidate = max(ocr_candidates, key=len)
        logger.info(f"🎯 MELHOR CANDIDATO ENCONTRADO: {best_candidate} [{len(best_candidate)} dígitos]")
        return best_candidate

    logger.warning("❌ Nenhum código numérico válido foi encontrado.")
    return ""