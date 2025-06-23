import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from ..db.session import SessionLocal  
from ..aspects.logging import DatabaseHandler

def setup_logging():
    """Configura o sistema de logging global"""
    
    # Cria diretório de logs se não existir
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configuração básica
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(
                "logs/app.log",
                maxBytes=1024*1024,  # 1MB
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    )
    
    # Adiciona handler para banco de dados
    db_handler = DatabaseHandler(SessionLocal())
    db_handler.setLevel(logging.INFO)
    db_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s - User: %(user_id)s'
    )
    db_handler.setFormatter(db_formatter)
    
    logging.getLogger().addHandler(db_handler)