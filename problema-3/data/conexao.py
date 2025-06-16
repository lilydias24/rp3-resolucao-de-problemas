"""
Módulo de conexão com o banco de dados SQLite.
"""
import sqlite3
import os
from typing import Optional

class ConexaoErro(Exception):
    """
    Exceção personalizada para erros de conexão com o banco de dados.
    """
    pass

def conectar() -> sqlite3.Connection:
    """
    Estabelece conexão com o banco de dados SQLite.
    
    Returns:
        sqlite3.Connection: Conexão com o banco de dados
        
    Raises:
        ConexaoErro: Se houver erro ao conectar
    """
    try:
        caminho_db = os.path.join(os.path.dirname(__file__), 'banco.db')
        conn = sqlite3.connect(caminho_db)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise ConexaoErro(f"Erro ao conectar ao banco de dados: {str(e)}")

def fechar_conexao(conn: Optional[sqlite3.Connection]) -> None:
    """
    Fecha a conexão com o banco de dados.
    
    Args:
        conn: Conexão a ser fechada
    """
    if conn:
        try:
            conn.close()
        except sqlite3.Error:
            pass  # Ignora erros ao fechar conexão

