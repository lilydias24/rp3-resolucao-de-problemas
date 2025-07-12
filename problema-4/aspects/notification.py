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
            # Adicionar lógica de notificação, ex: enviar e-mail
            logging.info(f"[ASPECT] Notificação enviada para {func.__name__}")
            return result
        except Exception as e:
            logging.error(f"[NOTIFICATION] Falha ao enviar notificação: {e}")
            raise
    return wrapper

def notify_on_event(func):
    """
    Aspecto para notificação de eventos que dispara print, log e e-mail.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            print(f"[NOTIFICATION] Executando {func.__name__}")
            logging.info(f"[NOTIFICATION] Iniciando execução de {func.__name__}")
            send_email_notification(f"Função {func.__name__} foi executada")
            
            result = func(*args, **kwargs)
            
            print(f"[NOTIFICATION] {func.__name__} executada com sucesso")
            logging.info(f"[NOTIFICATION] {func.__name__} executada com sucesso")
            send_email_notification(f"Função {func.__name__} executada com sucesso")
            
            return result
        except Exception as e:
            error_msg = f"Erro na execução de {func.__name__}: {e}"
            print(f"[NOTIFICATION] {error_msg}")
            logging.error(f"[NOTIFICATION] {error_msg}")
            send_email_notification(error_msg)
            raise
    return wrapper

def send_email_notification(message):
    """
    Função para envio de notificações por e-mail.
    Em uma implementação real, aqui seria feita a integração com serviço de e-mail.
    """
    # Simulação de envio de e-mail
    logging.info(f"[EMAIL] Notificação enviada: {message}")
    # Adicionar integração real com serviço de e-mail
    # Exemplo: smtp.send_message(...)
