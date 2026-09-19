# app/main.py

import sys
import ctypes
from PyQt6.QtWidgets import QApplication
from app.capture.overlay import SelectionOverlay
from app.capture.screen_capture import capture_region
from app.extraction.extractor import process_pipeline
from app.clipboard.manager import copy_to_clipboard
from app.hotkey.listener import GlobalHotkeyListener
from app.tray.system_tray import ScreenReaderTray
from app.utils.logger import logger

# Garante que o Windows identifique a aplicação como "Code Extract" nas notificações Toast
try:
    myappid = "codeextract.app.v1"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

class ScreenReaderApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Code Extract")
        self.app.setQuitOnLastWindowClosed(False)

        # 1. Overlay de seleção
        self.overlay = SelectionOverlay()
        self.overlay.region_selected.connect(self.handle_region_selected)

        # 2. Tray Icon
        self.tray = ScreenReaderTray()
        self.tray.capture_requested.connect(self.overlay.show_overlay)
        self.tray.quit_requested.connect(self.shutdown)
        self.tray.show()

        # 3. Escutador de Atalhos (Ctrl + Shift + C)
        self.hotkey_listener = GlobalHotkeyListener("<ctrl>+<shift>+c")
        self.hotkey_listener.hotkey_triggered.connect(self.overlay.show_overlay)
        self.hotkey_listener.start()

        logger.info("🚀 Code Extract pronto e ativo na System Tray! Pressione Ctrl + Shift + C")

    def handle_region_selected(self, x1: int, y1: int, x2: int, y2: int):
        img = capture_region(x1, y1, x2, y2)
        result_number = process_pipeline(img)

        if result_number:
            copy_to_clipboard(result_number)
            self.tray.notify_success(result_number)
        else:
            self.tray.notify_warning("Nenhum código numérico foi identificado.")

    def shutdown(self):
        logger.info("Encerrando Code Extract...")
        self.hotkey_listener.stop()
        self.app.quit()

    def run(self):
        sys.exit(self.app.exec())

def main():
    screen_reader = ScreenReaderApp()
    screen_reader.run()

if __name__ == "__main__":
    main()