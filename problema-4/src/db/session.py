"""
Módulo de configuração da sessão do banco de dados SQLAlchemy para uso com FastAPI.
Inclui a dependência get_db para injeção de sessão nas rotas.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

SQLALCHEMY_DATABASE_URL = "postgresql://localhost:postgres@localhost/problema-4"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependência do FastAPI para fornecer uma sessão do banco de dados.
    Garante que a sessão seja fechada após o uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()