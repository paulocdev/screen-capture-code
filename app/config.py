import os

# Atalho global principal
HOTKEY = "<ctrl>+<shift>+c"

# Dimensões mínimas para considerar uma seleção válida (px)
MIN_SELECTION_WIDTH = 10
MIN_SELECTION_HEIGHT = 10

# Caminho Padrão do Tesseract OCR no Windows
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Ângulos de rotação a testar no pipeline de extração
ROTATION_ANGLES = [0, 90, 270]