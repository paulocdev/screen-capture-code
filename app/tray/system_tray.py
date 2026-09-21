# app/tray/system_tray.py

import os
import sys
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap, QColor, QPainter
from PyQt6.QtCore import pyqtSignal
import logging

logger = logging.getLogger("ScreenReader")

def create_default_icon() -> QIcon:
    """Gera um ícone básico azul em memória caso o arquivo .ico não seja encontrado."""
    pixmap = QPixmap(32, 32)
    pixmap.fill(QColor(0, 0, 0, 0))
    painter = QPainter(pixmap)
    painter.setBrush(QColor(0, 120, 215))
    painter.setPen(QColor(255, 255, 255))
    painter.drawRoundedRect(2, 2, 28, 28, 6, 6)
    painter.drawText(pixmap.rect(), 0x0084, "CE")
    painter.end()
    return QIcon(pixmap)

def get_app_icon() -> QIcon:
    """Carrega o icone.ico da pasta do projeto ou de dentro do executável (.exe)."""
    if hasattr(sys, '_MEIPASS'):
        icon_path = os.path.join(sys._MEIPASS, 'icone.ico')
    else:
        icon_path = os.path.join(os.path.dirname(__file__), '..', '..', 'icone.ico')

    if os.path.exists(icon_path):
        return QIcon(icon_path)
    return create_default_icon()

class ScreenReaderTray(QSystemTrayIcon):
    capture_requested = pyqtSignal()
    quit_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # AQUI: Define o ícone personalizado da bandeja (System Tray)
        self.setIcon(get_app_icon())
        
        self.setToolTip("Code Extract — Rodando em segundo plano")

        menu = QMenu()
        
        capture_action = menu.addAction("Capturar (Ctrl+Shift+C)")
        capture_action.triggered.connect(self.capture_requested.emit)

        menu.addSeparator()

        quit_action = menu.addAction("Sair")
        quit_action.triggered.connect(self.quit_requested.emit)

        self.setContextMenu(menu)

    def notify_success(self, text: str):
        preview = text[:30] + "..." if len(text) > 30 else text
        self.showMessage(
            "Code Extract",
            f"Copiado para o Clipboard: {preview}",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )

    def notify_warning(self, message: str):
        self.showMessage(
            "Code Extract",
            message,
            QSystemTrayIcon.MessageIcon.Warning,
            2000
        )