# app/main.py

import sys
from PyQt6.QtWidgets import QApplication
from app.capture.overlay import SelectionOverlay
from app.capture.screen_capture import capture_region
from app.extraction.ocr import run_ocr
from app.extraction.extractor import extract_numbers_from_text
from app.utils.logger import logger

def on_region_selected(x1: int, y1: int, x2: int, y2: int):
    # 1. Capturar imagem da área selecionada
    img = capture_region(x1, y1, x2, y2)
    
    # 2. Executar OCR
    raw_text = run_ocr(img)
    logger.info(f"Texto bruto detectado:\n{raw_text.strip()}")

    # 3. Extrair e normalizar código numérico
    result_number = extract_numbers_from_text(raw_text)
    
    if result_number:
        logger.info(f"🎯 RESULTADO EXTRAÍDO: {result_number}")
    else:
        logger.warning("❌ Nenhum código numérico foi extraído.")
    
    QApplication.quit()

def main():
    app = QApplication(sys.argv)
    logger.info("Iniciando Screen Reader — FASE 2 & 3 (OCR + Extração)")

    overlay = SelectionOverlay()
    overlay.region_selected.connect(on_region_selected)
    overlay.show_overlay()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()