"""
Módulo de conexão com o banco de dados SQLite.
Fornece uma função para obter a conexão com o arquivo `data/banco.db`.
"""

import sqlite3
<<<<<<< HEAD
import os
=======
>>>>>>> origin/development

def conectar():
    """
    Estabelece uma conexão com o banco de dados SQLite do sistema.

    Returns:
        sqlite3.Connection: Objeto de conexão com o banco de dados.
    """
<<<<<<< HEAD
    caminho_db = os.path.join(os.path.dirname(__file__), 'banco.db')
    return sqlite3.connect(caminho_db)

=======
    return sqlite3.connect("data/banco.db")
>>>>>>> origin/development
