"""
Aspecto para envio de notificações automáticas em eventos importantes do sistema.
Pode ser expandido para enviar e-mail, mensagem, log, etc.
"""

import aspectlib
import logging
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

# Configurações de e-mail (ajuste conforme necessário)
EMAIL_FROM = "notificador@exemplo.com"
EMAIL_TO = "destinatario@exemplo.com"
EMAIL_SUBJECT = "Notificação do Sistema"
SMTP_SERVER = "localhost"  # ou "smtp.gmail.com" etc.
SMTP_PORT = 25  # 587 para TLS, 465 para SSL
SMTP_USER = None  # Se necessário
SMTP_PASS = None  # Se necessário


def send_email_notification(message: str):
    """
    Envia uma notificação por e-mail com o texto fornecido.
    """
    try:
        msg = MIMEText(message)
        msg['Subject'] = EMAIL_SUBJECT
        msg['From'] = formataddr(("Sistema de Notificação", EMAIL_FROM))
        msg['To'] = EMAIL_TO
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            if SMTP_USER and SMTP_PASS:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
        logging.info(f"[NOTIFICATION] E-mail enviado para {EMAIL_TO}")
    except Exception as e:
        logging.error(f"[NOTIFICATION] Falha ao enviar e-mail: {e}")

@aspectlib.Aspect
def notify_on_event(cutpoint, *args, **kwargs):
    """
    Aspecto que envia uma notificação (print e e-mail) sempre que a função decorada é executada com sucesso.
    """
    result = yield
    nome = getattr(cutpoint, '__name__', cutpoint.__class__.__name__)
    mensagem = f"Notificação: {nome} executada com sucesso."
    # Notificação por print
    print(mensagem)
    # Notificação por e-mail
    send_email_notification(mensagem)
    # Notificação por log
    logging.info(f"[NOTIFICATION] {mensagem}")
    return result
