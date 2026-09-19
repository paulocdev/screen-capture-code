# app/main.py

import sys
from PyQt6.QtWidgets import QApplication
from app.capture.overlay import SelectionOverlay
from app.capture.screen_capture import capture_region
from app.extraction.extractor import process_pipeline
from app.clipboard.manager import copy_to_clipboard
from app.utils.logger import logger

def on_region_selected(x1: int, y1: int, x2: int, y2: int):
    img = capture_region(x1, y1, x2, y2)
    result_number = process_pipeline(img)
    
    if result_number:
        copy_to_clipboard(result_number)
    else:
        logger.warning("❌ Nenhuma informação foi enviada para a área de transferência.")
    
    QApplication.quit()

def main():
    app = QApplication(sys.argv)
    logger.info("Iniciando Screen Reader — FASES 1 a 7 Integradas")

    overlay = SelectionOverlay()
    overlay.region_selected.connect(on_region_selected)
    overlay.show_overlay()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()