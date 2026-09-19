from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QRect, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen
from app.config import MIN_SELECTION_WIDTH, MIN_SELECTION_HEIGHT
import logging

logger = logging.getLogger("ScreenReader")

class SelectionOverlay(QWidget):
    # Sinal emitido quando a seleção for concluída: (x1, y1, x2, y2)
    region_selected = pyqtSignal(int, int, int, int)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setCursor(Qt.CursorShape.CrossCursor)

        self.begin = None
        self.end = None
        self.is_selecting = False

    def show_overlay(self):
        """Calcula a geometria total de todos os monitores e exibe o overlay."""
        virtual_rect = QRect()
        for screen in QApplication.screens():
            virtual_rect = virtual_rect.united(screen.geometry())

        self.setGeometry(virtual_rect)
        self.begin = None
        self.end = None
        self.is_selecting = False
        self.show()
        self.activateWindow()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.begin = event.globalPosition().toPoint()
            self.end = self.begin
            self.is_selecting = True
            self.update()

    def mouseMoveEvent(self, event):
        if self.is_selecting:
            self.end = event.globalPosition().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.is_selecting:
            self.end = event.globalPosition().toPoint()
            self.is_selecting = False
            self.hide()

            x1, y1 = self.begin.x(), self.begin.y()
            x2, y2 = self.end.x(), self.end.y()

            x_min, x_max = min(x1, x2), max(x1, x2)
            y_min, y_max = min(y1, y2), max(y1, y2)

            width = x_max - x_min
            height = y_max - y_min

            if width >= MIN_SELECTION_WIDTH and height >= MIN_SELECTION_HEIGHT:
                logger.info(f"Área selecionada: ({x_min}, {y_min}) -> ({x_max}, {y_max}) [{width}x{height}px]")
                self.region_selected.emit(x_min, y_min, x_max, y_max)
            else:
                logger.warning("Seleção ignorada (dimensões menores que o mínimo permitido).")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            logger.info("Seleção cancelada pelo usuário (ESC).")
            self.hide()

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Fundo escurecido semi-transparente
        painter.fillRect(self.rect(), QColor(0, 0, 0, 110))

        if self.begin and self.end:
            # Mapeia as coordenadas globais para as coordenadas locais da janela
            local_begin = self.mapFromGlobal(self.begin)
            local_end = self.mapFromGlobal(self.end)
            selection_rect = QRect(local_begin, local_end).normalized()

            # Recorta a área selecionada para torná-la 100% transparente
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.fillRect(selection_rect, Qt.GlobalColor.transparent)

            # Desenha a borda da seleção em azul
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
            pen = QPen(QColor(0, 120, 215), 2, Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            painter.drawRect(selection_rect)