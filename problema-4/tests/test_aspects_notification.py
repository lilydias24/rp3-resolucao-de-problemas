"""
Testes automatizados para o aspecto de notificações (notify_on_event).
Garante que notificações são enviadas ao executar funções importantes (print, log e e-mail).
"""
import pytest
from unittest.mock import patch
from aspects.notification import notify_on_event
import aspectlib

def fake_action():
    return "feito"

def test_notify_on_event():
    """
    Garante que o aspecto de notificação dispara print, log e e-mail.
    """
    with patch("builtins.print") as mock_print, \
         patch("logging.info") as mock_log, \
         patch("aspects.notification.send_email_notification") as mock_email:
        with aspectlib.weave(fake_action, notify_on_event):
            result = fake_action()
        assert result == "feito"
        assert mock_print.called
        assert mock_log.called
        assert mock_email.called
