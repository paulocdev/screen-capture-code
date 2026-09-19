# app/main.py

import sys
from PyQt6.QtWidgets import QApplication
from app.capture.overlay import SelectionOverlay
from app.capture.screen_capture import capture_region
from app.extraction.extractor import process_pipeline
from app.utils.logger import logger

def on_region_selected(x1: int, y1: int, x2: int, y2: int):
    # 1. Capturar imagem da área selecionada
    img = capture_region(x1, y1, x2, y2)
    
    # 2. Executar Pipeline (Rotação + Barcode + Preprocessing + OCR)
    result_number = process_pipeline(img)
    
    if result_number:
        logger.info(f"🎯 RESULTADO FINAL EXTRAÍDO: {result_number}")
    else:
        logger.warning("❌ Nenhum código numérico foi extraído.")
    
    QApplication.quit()

def main():
    app = QApplication(sys.argv)
    logger.info("Iniciando Screen Reader — FASES 1 a 6 integradas")

    overlay = SelectionOverlay()
    overlay.region_selected.connect(on_region_selected)
    overlay.show_overlay()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()