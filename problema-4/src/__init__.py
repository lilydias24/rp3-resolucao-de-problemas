"""Módulo principal da aplicação"""
from .db import init_db 
from .config import settings

__all__ = ['init_db', 'settings'] 