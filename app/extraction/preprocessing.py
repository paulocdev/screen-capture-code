# app/extraction/preprocessing.py

import cv2
import numpy as np
from PIL import Image

def pil_to_cv2(pil_img: Image.Image) -> np.ndarray:
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

def cv2_to_pil(cv_img: np.ndarray) -> Image.Image:
    if len(cv_img.shape) == 2:
        return Image.fromarray(cv_img)
    return Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

def rotate_image(cv_img: np.ndarray, angle: int) -> np.ndarray:
    if angle == 90:
        return cv2.rotate(cv_img, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 270:
        return cv2.rotate(cv_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif angle == 180:
        return cv2.rotate(cv_img, cv2.ROTATE_180)
    return cv_img

def enhance_for_ocr(cv_img: np.ndarray) -> np.ndarray:
    """
    Aumenta a resolução em 3x e aplica filtro de nitidez (sharpen)
    para definir as bordas de números pequenos ou com baixo contraste.
    """
    height, width = cv_img.shape[:2]
    # Amplia 3x com interpolação cúbica
    scaled = cv2.resize(cv_img, (width * 3, height * 3), interpolation=cv2.INTER_CUBIC)

    if len(scaled.shape) == 3:
        gray = cv2.cvtColor(scaled, cv2.COLOR_BGR2GRAY)
    else:
        gray = scaled

    # Matriz para reforço de nitidez nas bordas dos caracteres
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(gray, -1, kernel)

    # Threshold de Otsu para binarização limpa
    _, thresh = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh