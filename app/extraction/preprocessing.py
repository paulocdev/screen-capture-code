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
    Aplica escala 3x, filtro Unsharp Mask para desembaçar texto desfocado
    e binarização de Otsu.
    """
    height, width = cv_img.shape[:2]
    scaled = cv2.resize(cv_img, (width * 3, height * 3), interpolation=cv2.INTER_CUBIC)

    if len(scaled.shape) == 3:
        gray = cv2.cvtColor(scaled, cv2.COLOR_BGR2GRAY)
    else:
        gray = scaled

    # Unsharp Mask: remove o embaçado/desfocado de câmeras
    gaussian = cv2.GaussianBlur(gray, (0, 0), 2.0)
    unsharp = cv2.addWeighted(gray, 2.0, gaussian, -1.0, 0)

    # Binarização P&B pura
    _, thresh = cv2.threshold(unsharp, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh