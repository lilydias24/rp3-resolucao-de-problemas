"""
Testes automatizados para os aspectos de log_db_session e log_db_query.
Garante que sessões e queries do banco de dados são logadas corretamente.
"""
import pytest
from unittest.mock import patch
from aspects.db_session import log_db_session, log_db_query
import aspectlib
from sqlalchemy import text

def fake_db_op():
    return "ok"

def test_log_db_session_logs(db_session):
    """
    Garante que o aspecto log_db_session loga abertura e fechamento de sessão.
    """
    with patch("logging.info") as mock_log:
        with aspectlib.weave(fake_db_op, log_db_session):
            result = fake_db_op()
        assert result == "ok"
        calls = [c[0][0] for c in mock_log.call_args_list]
        assert any("Abrindo sessão" in msg for msg in calls)
        assert any("Sessão finalizada" in msg for msg in calls)

def test_log_db_query_logs_execute(db_session):
    """
    Garante que o aspecto log_db_query loga execução de queries (execute).
    """
    with patch("aspects.db_session.query_logger.info") as mock_log:
        with aspectlib.weave(db_session.execute, log_db_query):
            result = db_session.execute(text("SELECT 1"))
        assert result is not None
        calls = [c[0][0] for c in mock_log.call_args_list]
        assert any("[DB-QUERY] Executando query" in msg for msg in calls)
        assert any("Query executada com sucesso" in msg for msg in calls)

def test_log_db_query_logs_commit(db_session):
    """
    Garante que o aspecto log_db_query loga execução de commit.
    """
    with patch("aspects.db_session.query_logger.info") as mock_log:
        with aspectlib.weave(db_session.commit, log_db_query):
            db_session.begin()
            db_session.commit()
        calls = [c[0][0] for c in mock_log.call_args_list]
        assert any("[DB-QUERY] Executando query" in msg for msg in calls)
        assert any("Query executada com sucesso" in msg for msg in calls)

def test_log_db_query_logs_rollback(db_session):
    """
    Garante que o aspecto log_db_query loga execução de rollback.
    """
    with patch("aspects.db_session.query_logger.info") as mock_log:
        with aspectlib.weave(db_session.rollback, log_db_query):
            db_session.begin()
            db_session.rollback()
        calls = [c[0][0] for c in mock_log.call_args_list]
        assert any("[DB-QUERY] Executando query" in msg for msg in calls)
        assert any("Query executada com sucesso" in msg for msg in calls)
