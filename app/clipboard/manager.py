# app/clipboard/manager.py

import pyperclip
import logging

logger = logging.getLogger("ScreenReader")

def copy_to_clipboard(text: str) -> bool:
    """Copia a string informada diretamente para a Área de Transferência do sistema."""
    if not text:
        return False
    try:
        pyperclip.copy(text)
        logger.info("📋 Código copiado automaticamente para a área de transferência! (Pressione Ctrl + V)")
        return True
    except Exception as e:
        logger.error(f"Erro ao copiar para a área de transferência: {e}")
        return False