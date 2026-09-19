from PIL import Image
import mss
import logging

logger = logging.getLogger("ScreenReader")

def capture_region(x1: int, y1: int, x2: int, y2: int) -> Image.Image:
    """
    Captura a região selecionada garantindo suporte a múltiplos monitores,
    incluindo coordenadas negativas de telas secundárias.
    """
    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    # Evita erros de seleção de 0 pixels
    if width <= 0 or height <= 0:
        logger.warning("Seleção com dimensão inválida.")
        return Image.new("RGB", (1, 1))

    with mss.mss() as sct:
        monitor = {
            "top": top,
            "left": left,
            "width": width,
            "height": height
        }
        sct_img = sct.grab(monitor)
        # Converte a captura do mss para uma imagem PIL tratável pelo OpenCV
        return Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")