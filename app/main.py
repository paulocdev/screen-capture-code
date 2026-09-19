import sys
from PyQt6.QtWidgets import QApplication
from app.capture.overlay import SelectionOverlay
from app.capture.screen_capture import capture_region
from app.utils.logger import logger

def on_region_selected(x1: int, y1: int, x2: int, y2: int):
    # Captura a imagem PIL da região selecionada
    img = capture_region(x1, y1, x2, y2)
    
    # Salva temporariamente na raiz para validação da FASE 1
    output_filename = "captured_test.png"
    img.save(output_filename)
    logger.info(f"✅ Sucesso! Imagem salva como '{output_filename}'. FASE 1 concluída!")
    
    QApplication.quit()

def main():
    app = QApplication(sys.argv)
    logger.info("Iniciando Screen Reader — FASE 1 (MVP de Captura)")

    overlay = SelectionOverlay()
    overlay.region_selected.connect(on_region_selected)
    overlay.show_overlay()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()