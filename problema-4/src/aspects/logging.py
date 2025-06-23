import logging
from datetime import datetime
from aspectlib import Aspect
from sqlalchemy.orm import Session
from typing import Dict, Any

# Configuração básica do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger(__name__)

class DatabaseHandler(logging.Handler):
    """Handler customizado para salvar logs no banco"""
    
    def __init__(self, db: Session):
        super().__init__()
        self.db = db
    
    def emit(self, record):
        from src.db.models import SystemLog
        
        log_entry = SystemLog(
            action=record.funcName,
            user_id=getattr(record, 'user_id', None),
            details=self.format(record),
            level=record.levelname,
            created_at=datetime.now()
        )
        self.db.add(log_entry)
        self.db.commit()

@Aspect
def log_operations(*args, **kwargs):
    """Aspecto principal para log de operações"""
    
    # Extrai informações do contexto
    target = args[0] if args else None
    class_name = target.__class__.__name__ if target else "Global"
    method_name = args[1].__name__ if len(args) > 1 else args[0].__name__
    
    # Prepara informações extras
    extra_info = {
        'user_id': kwargs.get('current_user').user_id if 'current_user' in kwargs else None,
        'entity_type': class_name,
        'entity_id': kwargs.get('id', kwargs.get('product_id', None))
    }
    
    # Log antes da execução
    logger.info(
        f"Iniciando {class_name}.{method_name}",
        extra=extra_info
    )
    
    try:
        result = yield
        # Log após execução bem-sucedida
        logger.info(
            f"{class_name}.{method_name} executado com sucesso",
            extra={**extra_info, 'result': str(result)[:100]}  # Limita tamanho do log
        )
        return result
        
    except Exception as e:
        # Log em caso de erro
        logger.error(
            f"Erro em {class_name}.{method_name}: {str(e)}",
            extra={**extra_info, 'error': str(e)},
            exc_info=True
        )
        raise