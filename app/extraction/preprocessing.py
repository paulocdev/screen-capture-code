# app/extraction/preprocessing.py

import cv2
import numpy as np
from PIL import Image

def pil_to_cv2(pil_img: Image.Image) -> np.ndarray:
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

def cv2_to_pil(cv_img: np.ndarray) -> Image.Image:
    # Se a imagem estiver em escala de cinza
    if len(cv_img.shape) == 2:
        return Image.fromarray(cv_img)
    return Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

def rotate_image(cv_img: np.ndarray, angle: int) -> np.ndarray:
    """Rotaciona a imagem no ângulo especificado (0, 90, 270)."""
    if angle == 90:
        return cv2.rotate(cv_img, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 270:
        return cv2.rotate(cv_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif angle == 180:
        return cv2.rotate(cv_img, cv2.ROTATE_180)
    return cv_img

def preprocess_image(cv_img: np.ndarray) -> np.ndarray:
    """Aplica redimensionamento 2x, escala de cinza e limiarização (threshold) para facilitar o OCR."""
    height, width = cv_img.shape[:2]
    # Redimensiona para aumentar a definição dos números
    resized = cv2.resize(cv_img, (width * 2, height * 2), interpolation=cv2.INTER_CUBIC)
    
    # Converte para escala de cinza se for imagem colorida
    if len(resized.shape) == 3:
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    else:
        gray = resized

    # Binarização de Otsu para destacar caracteres escuros em fundo claro
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh