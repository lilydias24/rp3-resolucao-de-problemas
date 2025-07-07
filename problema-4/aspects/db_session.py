import logging
from functools import wraps

"""
Aspectos para logar abertura/fechamento de sessão e queries SQL do banco de dados.
"""

def log_db_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"[DB-SESSION] Executando operação: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def log_db_query(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"[DB-QUERY] Executando query: args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"[DB-QUERY] Query executada com sucesso")
        return result
    return wrapper 