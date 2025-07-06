import aspectlib
import logging
from sqlalchemy.orm import Session

"""
Aspectos para logar abertura/fechamento de sessão e queries SQL do banco de dados.
"""

@aspectlib.Aspect
def log_db_session(cutpoint, *args, **kwargs):
    """
    Aspecto para logar abertura e fechamento de sessões com o banco de dados.
    """
    logging.info("[DB-SESSION] Abrindo sessão com o banco de dados")
    try:
        result = yield
        logging.info("[DB-SESSION] Sessão finalizada com sucesso")
        return result
    except Exception as e:
        logging.error(f"[DB-SESSION] Erro na sessão: {e}")
        raise

@aspectlib.Aspect
def log_db_query(cutpoint, *args, **kwargs):
    """
    Aspecto para logar execução de queries SQL (execute, commit, rollback).
    """
    logging.info(f"[DB-QUERY] Executando query: args={args}, kwargs={kwargs}")
    try:
        result = yield
        logging.info("[DB-QUERY] Query executada com sucesso")
        return result
    except Exception as e:
        logging.error(f"[DB-QUERY] Erro ao executar query: {e}")
        raise 