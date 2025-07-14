"""
Módulo de configuração da sessão do banco de dados SQLAlchemy para uso com FastAPI.
Inclui a dependência get_db para injeção de sessão nas rotas.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import os
from aspects.db_session import log_db_session, log_db_query

# Configuração do banco de dados PostgreSQL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:root@localhost:5432/problema4")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"options": "-c client_encoding=utf8"}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@log_db_session
def get_db():
    """
    Dependência do FastAPI para fornecer uma sessão do banco de dados.
    Garante que a sessão seja fechada após o uso.
    Yields:
        db (Session): Sessão do banco de dados.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()