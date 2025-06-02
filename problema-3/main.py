"""
Sistema de recomendação de carreiras usando paradigma lógico.

Este módulo executa o fluxo principal do sistema:
- Coleta os interesses de um estudante via terminal
- Coleta o desempenho acadêmico do estudante
- Constrói os fatos lógicos a partir dos interesses e desempenho
- Salva os dados no banco SQLite
- Lista os estudantes registrados
"""
from utils.sistema import (
    exibir_menu_principal,
    cadastrar_estudante,
    gerenciar_estudantes,
    gerar_relatorios
)

def main():
    """
    Função principal que inicia o sistema.
    """
    while True:
        exibir_menu_principal()
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            cadastrar_estudante()
        elif opcao == "2":
            gerenciar_estudantes()
        elif opcao == "3":
            gerar_relatorios()
        elif opcao == "0":
            print("\nSaindo do sistema...")
            break
        else:
            print("\nOpção inválida! Tente novamente.")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()
