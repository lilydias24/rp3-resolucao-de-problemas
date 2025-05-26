"""
Módulo do fluxo principal do sistema.

Contém funções para gerenciar o fluxo de execução do sistema.
"""
from data.estudante_db import criar_tabela_estudantes, salvar_estudante, listar_estudantes
from logic.logica import gerar_fatos_de_interesses
from utils.interface import (
    coletar_interesses,
    coletar_desempenho_academico,
    exibir_fatos,
    exibir_estudantes
)

def exibir_menu():
    """
    Exibe o menu principal do sistema.
    """
    print("\n=== Sistema de Recomendação de Carreiras ===")
    print("1. Cadastrar novo estudante")
    print("2. Listar estudantes cadastrados")
    print("3. Sair")
    return input("\nEscolha uma opção: ").strip()

def cadastrar_estudante():
    """
    Executa o fluxo de cadastro de um novo estudante.
    """
    # Coleta dados do estudante
    estudante = coletar_interesses()
    estudante = coletar_desempenho_academico(estudante)
    
    # Processa os dados
    fatos = gerar_fatos_de_interesses(estudante)
    exibir_fatos(fatos)
    
    # Salva no banco
    salvar_estudante(estudante)
    print("\n Estudante cadastrado com sucesso! \n")

def executar_fluxo():
    """
    Executa o fluxo principal do sistema com menu interativo.
    """
    # Inicializa o banco de dados
    criar_tabela_estudantes()
    
    while True:
        opcao = exibir_menu()
        
        if opcao == "1":
            cadastrar_estudante()
        elif opcao == "2":
            estudantes = listar_estudantes()
            exibir_estudantes(estudantes)
        elif opcao == "3":
            print("\nEncerrando o sistema...")
            break
        else:
            print("\nOpção inválida! Por favor, escolha uma opção válida.") 