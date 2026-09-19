from PIL import Image, ImageGrab
import logging

logger = logging.getLogger("ScreenReader")

def capture_region(x1: int, y1: int, x2: int, y2: int) -> Image.Image:
    """
    Captura uma região específica da tela e retorna uma imagem PIL.
    Suporta múltiplos monitores via Pillow (all_screens=True).
    """
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)

    bbox = (x_min, y_min, x_max, y_max)
    logger.info(f"Capturando região da tela: {bbox}")

    image = ImageGrab.grab(bbox=bbox, all_screens=True)
    return image