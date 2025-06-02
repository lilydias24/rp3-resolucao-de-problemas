"""
Módulo principal do sistema de recomendação de carreiras.

Contém todas as funções e configurações do sistema, incluindo:
- Menus e interfaces
- Gerenciamento de estudantes
- Geração de relatórios
- Recomendações de carreiras
"""
import os
from logic.motor import MotorDeInferencia, criar_estudante
from data.estudante_db import listar_estudantes, excluir_estudante

def exibir_menu_principal():
    """
    Exibe o menu principal do sistema.
    """
    print("\n=== Sistema de Recomendação de Carreiras ===")
    print("1. Cadastrar novo estudante")
    print("2. Gerenciar estudantes")
    print("3. Gerar relatórios")
    print("0. Sair")
    print("==========================================")

def exibir_menu_gerenciamento():
    """
    Exibe o menu de gerenciamento de estudantes.
    """
    print("\n=== Gerenciamento de Estudantes ===")
    print("1. Listar todos os estudantes")
    print("2. Excluir estudante")
    print("0. Voltar")
    print("================================")

def exibir_recomendacoes(recomendadas, proximas):
    """
    Exibe as recomendações de carreira de forma mais detalhada e informativa.
    """
    print("\nCarreiras recomendadas:")
    if recomendadas:
        for c in recomendadas:
            print(f"\n- {c['carreira']} (score: {c['score']}%)")
            print(f"  Justificativa: {c['justificativa']}")
            print("\n  Explicação:")
            for tipo, explicacao in c['explicacao'].items():
                print(f"  - {explicacao}")
    else:
        print("\nNenhuma carreira recomendada no momento.")
        print("Para ter uma carreira recomendada, você precisa atender TODOS os critérios")
        print("(interesses, habilidades e desempenho) para pelo menos uma carreira.")
    
    print("\nCarreiras próximas:")
    if proximas:
        # Ordena as carreiras próximas pelo score
        proximas.sort(key=lambda x: x['score'], reverse=True)
        
        for c in proximas:
            print(f"\n- {c['carreira']} (score: {c['score']}%)")
            print(f"  Justificativa: {c['justificativa']}")
            print("\n  Explicação:")
            for tipo, explicacao in c['explicacao'].items():
                print(f"  - {explicacao}")
            
            # Adiciona sugestões de melhoria
            print("\n  Sugestões para transformar em carreira recomendada:")
            for tipo, explicacao in c['explicacao'].items():
                if "Faltam" in explicacao:
                    print(f"  - {explicacao.replace('Faltam', 'Adquira')}")
    else:
        print("Nenhuma carreira próxima no momento.")

def listar_todos_estudantes():
    """
    Lista todos os estudantes cadastrados no sistema.
    """
    print("\nEstudantes cadastrados:")
    print("----------------------")
    estudantes = listar_estudantes()
    if not estudantes:
        print("Nenhum estudante cadastrado.")
        return
    
    for estudante in estudantes:
        print(f"\nNome: {estudante['nome']}")
        print(f"Interesses: {', '.join(estudante['interesses'])}")
        if estudante['habilidades']:
            print(f"Habilidades: {', '.join(estudante['habilidades'])}")
        if estudante['desempenho']:
            print("Desempenho:")
            for disciplina, nota in estudante['desempenho'].items():
                print(f"  - {disciplina}: {nota}")

def excluir_estudante_sistema():
    """
    Interface para excluir um estudante do sistema.
    """
    print("\nExcluir estudante")
    print("----------------")
    nome = input("Digite o nome do estudante a ser excluído: ").strip()
    
    if not nome:
        print("Nome inválido!")
        return
    
    confirmacao = input(f"\nTem certeza que deseja excluir o estudante '{nome}'? (s/n): ").lower()
    if confirmacao != 's':
        print("Operação cancelada.")
        return
    
    if excluir_estudante(nome):
        print(f"Estudante '{nome}' foi excluído com sucesso!")
    else:
        print(f"Não foi possível excluir o estudante '{nome}'.")

def gerenciar_estudantes():
    """
    Função que gerencia o menu de estudantes.
    """
    while True:
        exibir_menu_gerenciamento()
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            listar_todos_estudantes()
        elif opcao == "2":
            excluir_estudante_sistema()
        elif opcao == "0":
            break
        else:
            print("\nOpção inválida! Tente novamente.")
        
        input("\nPressione Enter para continuar...")

def cadastrar_estudante():
    """
    Função que gerencia o cadastro de um novo estudante.
    """
    CAMINHO_REGRAS = os.path.join(os.path.dirname(__file__), 'data', 'regras.json')
    estudante = criar_estudante(CAMINHO_REGRAS)
    motor = MotorDeInferencia(CAMINHO_REGRAS)
    recomendadas, proximas = motor.processa_estudante(estudante)
    
    exibir_recomendacoes(recomendadas, proximas)

def gerar_relatorios():
    """
    Função que gera os relatórios do sistema.
    """
    try:
        from reports.gerar_relatorios import gerar_relatorios
        gerar_relatorios()
    except ImportError:
        print("\nErro: Módulo de relatórios não encontrado.")
        print("Certifique-se de que o módulo reports está instalado corretamente.")