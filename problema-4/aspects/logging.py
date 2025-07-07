import logging
import os
import sys
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Dict, Any
from functools import wraps

"""
Aspectos de logging para registrar operações importantes da aplicação.
Inclui handler customizado para logs em banco e aspectos para log de operações e tratamento de erros.
"""

print("DEBUG: Entrou em src/aspects/logging.py")
print("DEBUG: PYTEST_CURRENT_TEST =", os.environ.get("PYTEST_CURRENT_TEST"))

if "pytest" in sys.modules or os.environ.get("PYTEST_CURRENT_TEST"):
    print("DEBUG: DatabaseHandler DUMMY ativado para testes")
    class DatabaseHandler(logging.Handler):
        """Handler dummy para testes (não faz nada)."""
        def __init__(self, db: Session):
            super().__init__()
        def emit(self, record):
            pass
    logger = logging.getLogger(__name__)
else:
    print("DEBUG: DatabaseHandler REAL ativado (produção)")
    # Configuração básica do logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='app.log'
    )
    logger = logging.getLogger(__name__)
    class DatabaseHandler(logging.Handler):
        """Handler customizado para salvar logs no banco de dados."""
        def __init__(self, db: Session):
            super().__init__()
            self.db = db
        def emit(self, record):
            from src.db.models import SystemLog
            log_entry = SystemLog(
                action=record.funcName,
                user_id=getattr(record, 'user_id', None),
                details=record.getMessage(),
                level=record.levelname,
                created_at=datetime.now()
            )
            self.db.add(log_entry)
            self.db.commit()

def logging_aspect(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"[ASPECT] Entrando em {func.__name__} com args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"[ASPECT] Saindo de {func.__name__} com resultado={result}")
        return result
    return wrapper
