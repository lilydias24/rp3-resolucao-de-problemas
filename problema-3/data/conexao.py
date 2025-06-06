"""
Módulo de conexão com o banco de dados SQLite.
Fornece uma função para obter a conexão com o arquivo `data/banco.db`.
"""

import sqlite3
import os

def conectar():
    """
    Estabelece uma conexão com o banco de dados SQLite do sistema.

    Returns:
        sqlite3.Connection: Objeto de conexão com o banco de dados.
    """
    caminho_db = os.path.join(os.path.dirname(__file__), 'banco.db')
    return sqlite3.connect(caminho_db)
