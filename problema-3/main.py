"""
Sistema de recomendação de carreiras usando paradigma lógico.

Este módulo executa o fluxo principal do sistema:
- Coleta os interesses de um estudante via terminal
- Coleta o desempenho acadêmico do estudante
- Constrói os fatos lógicos a partir dos interesses e desempenho
- Salva os dados no banco SQLite
- Lista os estudantes registrados
"""
from utils.sistema import executar_fluxo

def main():
    """
    Função principal que inicia o sistema.
    """
    executar_fluxo()

if __name__ == "__main__":
    main()
