"""
Módulo de conexão com o banco de dados SQLite.
"""
import sqlite3
<<<<<<< HEAD
import os
=======
>>>>>>> origin/development

def conectar() -> sqlite3.Connection:
    """
    Estabelece conexão com o banco de dados SQLite.
    
    Returns:
        sqlite3.Connection: Conexão com o banco de dados
        
    Raises:
        ConexaoErro: Se houver erro ao conectar
    """
<<<<<<< HEAD
    caminho_db = os.path.join(os.path.dirname(__file__), 'banco.db')
    return sqlite3.connect(caminho_db)

=======
    return sqlite3.connect("data/banco.db")
>>>>>>> origin/development
