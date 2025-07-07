"""
Módulo de inicialização do banco de dados, expõe Base, SessionLocal e função para criar tabelas.
"""
from .base import Base
from .session import SessionLocal, engine
from .models import * 

def init_db():
    """Cria todas as tabelas no banco de dados"""
    Base.metadata.create_all(bind=engine)

__all__ = ['SessionLocal', 'Base', 'init_db']