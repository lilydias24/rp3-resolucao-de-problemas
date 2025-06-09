"""
Módulo para gerenciar conexões com o banco de dados SQLite.
"""
import sqlite3
from typing import Optional
from .transacao import ConexaoErro

class GerenciadorConexao:
    """
    Classe para gerenciar conexões com o banco de dados usando o padrão Singleton.
    """
    _instancia = None
    _conexao = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(GerenciadorConexao, cls).__new__(cls)
        return cls._instancia

    def _criar_conexao(self) -> sqlite3.Connection:
        """
        Cria uma nova conexão com o banco de dados.
        
        Returns:
            Conexão com o banco de dados
            
        Raises:
            ConexaoErro: Se houver erro ao criar a conexão
        """
        try:
            conexao = sqlite3.connect('data/banco.db')
            conexao.row_factory = sqlite3.Row
            conexao.execute("PRAGMA foreign_keys = ON")
            return conexao
        except Exception as e:
            raise ConexaoErro(f"Erro ao criar conexão com o banco: {str(e)}")

    def obter_conexao(self) -> sqlite3.Connection:
        """
        Retorna a conexão atual ou cria uma nova se necessário.
        
        Returns:
            Conexão com o banco de dados
            
        Raises:
            ConexaoErro: Se houver erro ao obter a conexão
        """
        try:
            if self._conexao is None:
                self._conexao = self._criar_conexao()
            return self._conexao
        except Exception as e:
            raise ConexaoErro(f"Erro ao obter conexão: {str(e)}")

    def fechar_conexao(self) -> None:
        """
        Fecha a conexão atual se estiver aberta.
        
        Raises:
            ConexaoErro: Se houver erro ao fechar a conexão
        """
        try:
            if self._conexao is not None:
                self._conexao.close()
                self._conexao = None
        except Exception as e:
            raise ConexaoErro(f"Erro ao fechar conexão: {str(e)}")

def conectar() -> sqlite3.Connection:
    """
    Retorna uma conexão com o banco de dados.
    
    Returns:
        Conexão com o banco de dados
        
    Raises:
        ConexaoErro: Se houver erro ao conectar
    """
    return GerenciadorConexao().obter_conexao()

def desconectar() -> None:
    """
    Fecha a conexão atual com o banco de dados.
    
    Raises:
        ConexaoErro: Se houver erro ao desconectar
    """
    GerenciadorConexao().fechar_conexao()
