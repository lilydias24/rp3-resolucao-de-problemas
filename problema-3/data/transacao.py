"""
Módulo para gerenciamento de transações e tratamento de erros no banco de dados.
"""
from typing import Dict, List, Tuple, Any, Optional
import sqlite3
from contextlib import contextmanager
from data.conexao import ConexaoErro

class BancoErro(Exception):
    """Exceção base para erros do banco de dados."""
    pass

class TransacaoErro(BancoErro):
    """Erro durante uma transação."""
    pass

class ConsultaErro(BancoErro):
    """Erro durante uma consulta."""
    pass

@contextmanager
def transacao(conexao: sqlite3.Connection):
    """
    Gerenciador de contexto para transações.
    
    Args:
        conexao: Conexão com o banco de dados
        
    Yields:
        Cursor da conexão
        
    Raises:
        TransacaoErro: Se ocorrer erro durante a transação
    """
    cursor = conexao.cursor()
    try:
        yield cursor
        conexao.commit()
    except Exception as e:
        conexao.rollback()
        raise TransacaoErro(f"Erro na transação: {str(e)}")
    finally:
        cursor.close()

def executar_consulta(conexao: sqlite3.Connection, query: str, params: tuple = ()) -> list:
    """
    Executa uma consulta SQL com tratamento de erros.
    
    Args:
        conexao: Conexão com o banco de dados
        query: Query SQL a ser executada
        params: Parâmetros da query
        
    Returns:
        Lista de resultados
        
    Raises:
        ConsultaErro: Se ocorrer erro durante a consulta
    """
    try:
        with transacao(conexao) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    except Exception as e:
        raise ConsultaErro(f"Erro na consulta: {str(e)}")

def executar_comando(conexao: sqlite3.Connection, query: str, params: tuple = ()) -> int:
    """
    Executa um comando SQL com tratamento de erros.
    
    Args:
        conexao: Conexão com o banco de dados
        query: Comando SQL a ser executado
        params: Parâmetros do comando
        
    Returns:
        Número de linhas afetadas
        
    Raises:
        ConsultaErro: Se ocorrer erro durante o comando
    """
    try:
        with transacao(conexao) as cursor:
            cursor.execute(query, params)
            return cursor.rowcount
    except Exception as e:
        raise ConsultaErro(f"Erro no comando: {str(e)}")

def executar_script(conexao: sqlite3.Connection, script: str) -> None:
    """
    Executa um script SQL com tratamento de erros.
    
    Args:
        conexao: Conexão com o banco de dados
        script: Script SQL a ser executado
        
    Raises:
        ConsultaErro: Se ocorrer erro durante o script
    """
    try:
        with transacao(conexao) as cursor:
            cursor.executescript(script)
    except Exception as e:
        raise ConsultaErro(f"Erro no script: {str(e)}")

def verificar_tabela(conexao: sqlite3.Connection, nome_tabela: str) -> bool:
    """
    Verifica se uma tabela existe no banco de dados.
    
    Args:
        conexao: Conexão com o banco de dados
        nome_tabela: Nome da tabela a ser verificada
        
    Returns:
        True se a tabela existe, False caso contrário
    """
    try:
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        resultado = executar_consulta(conexao, query, (nome_tabela,))
        return len(resultado) > 0
    except Exception:
        return False

def verificar_coluna(conexao: sqlite3.Connection, nome_tabela: str, nome_coluna: str) -> bool:
    """
    Verifica se uma coluna existe em uma tabela.
    
    Args:
        conexao: Conexão com o banco de dados
        nome_tabela: Nome da tabela
        nome_coluna: Nome da coluna
        
    Returns:
        True se a coluna existe, False caso contrário
    """
    try:
        query = "PRAGMA table_info(?)"
        colunas = executar_consulta(conexao, query, (nome_tabela,))
        return any(coluna[1] == nome_coluna for coluna in colunas)
    except Exception:
        return False 