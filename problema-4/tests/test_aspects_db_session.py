"""
Testes automatizados para os aspectos de log_db_session e log_db_query.
Garante que sessões e queries do banco de dados são logadas corretamente.
"""
import pytest

from unittest.mock import patch
from aspects.db_session import log_db_session, log_db_query

class DummySession:
    def execute(self, *args, **kwargs):
        return "executed"
    def commit(self):
        return "committed"
    def rollback(self):
        return "rolled back"

def test_log_db_session_logs():
    """
    Garante que o aspecto log_db_session loga abertura e fechamento de sessão.
    """
    @log_db_session
    def fake_db_op():
        return "ok"
    with patch("logging.info") as mock_log:
        result = fake_db_op()
        assert result == "ok"
        # Deve logar abertura e fechamento
        calls = [c[0][0] for c in mock_log.call_args_list]
        assert any("Abrindo sessão" in msg for msg in calls)
        assert any("Sessão finalizada" in msg for msg in calls)

def test_log_db_query_logs_execute():
    """
    Garante que o aspecto log_db_query loga execução de queries (execute).
    """
    session = DummySession()
    wrapped_execute = log_db_query(session.execute)
    with patch("logging.info") as mock_log:
        result = wrapped_execute()
        assert result == "executed"
        calls = [c[0][0] for c in mock_log.call_args_list]
        assert any("[DB-QUERY] Executando query" in msg for msg in calls)
        assert any("Query executada com sucesso" in msg for msg in calls)

def test_log_db_query_logs_commit():
    """
    Garante que o aspecto log_db_query loga execução de commit.
    """
    session = DummySession()
    wrapped_commit = log_db_query(session.commit)
    with patch("logging.info") as mock_log:
        result = wrapped_commit()
        assert result == "committed"
        calls = [c[0][0] for c in mock_log.call_args_list]
        assert any("[DB-QUERY] Executando query" in msg for msg in calls)
        assert any("Query executada com sucesso" in msg for msg in calls)

def test_log_db_query_logs_rollback():
    """
    Garante que o aspecto log_db_query loga execução de rollback.
    """
    session = DummySession()
    wrapped_rollback = log_db_query(session.rollback)
    with patch("logging.info") as mock_log:
        result = wrapped_rollback()
        assert result == "rolled back"
        calls = [c[0][0] for c in mock_log.call_args_list]
        assert any("[DB-QUERY] Executando query" in msg for msg in calls)
        assert any("Query executada com sucesso" in msg for msg in calls)
