from PyQt6.QtCore import QObject, pyqtSignal
from pynput import keyboard
import logging

logger = logging.getLogger("ScreenReader")

class GlobalHotkeyListener(QObject):
    # Sinal Qt seguro para acionar a interface a partir da thread do pynput
    hotkey_triggered = pyqtSignal()

    def __init__(self, hotkey_str: str = "<ctrl>+<shift>+c"):
        super().__init__()
        self.hotkey_str = hotkey_str
        self.listener = None

    def _on_activate(self):
        logger.info("Atalho global detectado! Exibindo overlay...")
        self.hotkey_triggered.emit()

    def start(self):
        """Inicia a escuta do atalho em uma thread em segundo plano."""
        try:
            hotkey_map = {self.hotkey_str: self._on_activate}
            self.listener = keyboard.GlobalHotKeys(hotkey_map)
            self.listener.start()
            logger.info(f"Escutador de atalho global iniciado: {self.hotkey_str}")
        except Exception as e:
            logger.error(f"Erro ao iniciar atalho global: {e}")

    def stop(self):
        if self.listener:
            self.listener.stop()