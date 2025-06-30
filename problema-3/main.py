"""
Módulo principal do sistema.

Contém a função main() que inicia o sistema.
"""
import sys
import os
from typing import Dict, List, Tuple, Any
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.conexao import conectar, ConexaoErro
from data.criar_banco import criar_tabelas
from logic.controlador import Controlador
from utils.interface import Interface

def main() -> None:
    """
    Função principal do sistema.
    """
    try:
        # Inicializa o banco
        criar_tabelas()
        
        # Conecta ao banco
        conectar()
        
        # Inicializa o controlador
        controlador = Controlador()
        
        # Executa o sistema
        controlador.executar()
        
    except ConexaoErro as e:
        Interface.exibir_erro(f"Erro de conexão com o banco de dados: {str(e)}")
        sys.exit(1)
    except Exception as e:
        Interface.exibir_erro(f"Erro inesperado: {str(e)}")
        sys.exit(1)
    finally:
        Interface.exibir_sucesso("\nSistema finalizado com sucesso!")

if __name__ == "__main__":
    main()
