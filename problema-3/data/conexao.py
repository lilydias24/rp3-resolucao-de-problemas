"""
Módulo de conexão com o banco de dados SQLite.
Fornece uma função para obter a conexão com o arquivo `data/banco.db`.
"""

import sqlite3

def conectar():
    """
    Estabelece uma conexão com o banco de dados SQLite do sistema.

    Returns:
        sqlite3.Connection: Objeto de conexão com o banco de dados.
    """
    return sqlite3.connect("data/banco.db")
