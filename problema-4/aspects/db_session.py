import logging
from functools import wraps

"""
Aspectos para logar abertura/fechamento de sessão e queries SQL do banco de dados.
"""

# Logger específico para queries
query_logger = logging.getLogger(__name__)

def log_db_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info("[DB-SESSION] Abrindo sessão")
        try:
            result = func(*args, **kwargs)
            logging.info("[DB-SESSION] Sessão finalizada")
            return result
        except Exception as e:
            logging.error(f"[DB-SESSION] Erro na sessão: {e}")
            raise
    return wrapper

def log_db_query(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        query_logger.info(f"[DB-QUERY] Executando query: args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            query_logger.info("[DB-QUERY] Query executada com sucesso")
            return result
        except Exception as e:
            query_logger.error(f"[DB-QUERY] Erro na query: {e}")
            raise
    return wrapper 