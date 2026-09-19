# app/extraction/barcode.py

from pyzbar.pyzbar import decode
from PIL import Image
import logging

logger = logging.getLogger("ScreenReader")

def read_barcode(image: Image.Image) -> str:
    """Tenta ler um código de barras diretamente da imagem usando pyzbar."""
    try:
        decoded_objects = decode(image)
        for obj in decoded_objects:
            data = obj.data.decode("utf-8")
            if data:
                logger.info(f"Código de barras detectado diretamente via PyZBar: {data}")
                return data
    except Exception as e:
        logger.debug(f"PyZBar não encontrou código de barras: {e}")
    return ""