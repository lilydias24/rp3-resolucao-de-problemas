"""
Aspecto para envio de notificações automáticas em eventos importantes do sistema.
Pode ser expandido para enviar e-mail, mensagem, log, etc.
"""

import logging
from functools import wraps

def notification_aspect(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            # Aqui você pode adicionar lógica de notificação, ex: enviar e-mail
            logging.info(f"[ASPECT] Notificação enviada para {func.__name__}")
            return result
        except Exception as e:
            logging.error(f"[NOTIFICATION] Falha ao enviar notificação: {e}")
            raise
    return wrapper
