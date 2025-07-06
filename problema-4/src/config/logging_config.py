"""
Configuração centralizada de logging para a aplicação FastAPI.
Inclui setup de logging rotativo em arquivo, console e integração com handler customizado para logs no banco de dados.
"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from ..db.session import SessionLocal  
import os

def setup_logging():
    """
    Configura o sistema de logging da aplicação.
    - Cria diretório de logs se necessário.
    - Adiciona handlers para arquivo rotativo e console.
    - Em produção, adiciona handler customizado para salvar logs no banco de dados.
    - Em ambiente de teste, evita logging em arquivo/banco.
    """
    print("DEBUG: Chamou setup_logging()")
    print("DEBUG: PYTEST_CURRENT_TEST =", os.environ.get("PYTEST_CURRENT_TEST"))
    if os.environ.get("PYTEST_CURRENT_TEST"):
        print("DEBUG: setup_logging() abortado em ambiente de teste")
        return
    
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
    
    # Só adiciona o handler customizado se NÃO estiver rodando testes
    if not os.environ.get("PYTEST_CURRENT_TEST"):
        from aspects.logging import DatabaseHandler
        db_handler = DatabaseHandler(SessionLocal())
        db_handler.setLevel(logging.INFO)
        db_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s - User: %(user_id)s'
        )
        db_handler.setFormatter(db_formatter)
        logging.getLogger().addHandler(db_handler)