"""
Módulo do fluxo principal do sistema.

Contém funções para gerenciar o fluxo de execução do sistema.
"""
import json
import os
from data.estudante_db import criar_tabela_estudantes, salvar_estudante, listar_estudantes
from logic.motor import MotorDeInferencia
from utils.interface import (
    coletar_interesses,
    coletar_habilidades,
    coletar_desempenho_academico,
    exibir_fatos,
    exibir_estudantes
)
from utils.gestor_interface import executar_menu_gestor

def exibir_menu():
    """
    Exibe o menu principal do sistema.
    """
    print("\n=== Sistema de Recomendação de Carreiras ===")
    print("1. Cadastrar novo estudante")
    print("2. Listar estudantes cadastrados")
    print("3. Buscar estudante por nome")
    print("4. Ver recomendações de carreira")
    print("5. Menu do Gestor Acadêmico")
    print("6. Sair")
    return input("\nEscolha uma opção: ").strip()

def cadastrar_estudante():
    """
    Executa o fluxo de cadastro de um novo estudante.
    """
    try:
       
        estudante = coletar_interesses()
        estudante = coletar_habilidades(estudante)
        estudante = coletar_desempenho_academico(estudante)
        
       
        salvar_estudante(estudante)
        print("\nEstudante cadastrado com sucesso! \n")
    except Exception as e:
        print(f"\nErro ao cadastrar estudante: {str(e)}")

def buscar_estudante():
    """
    Busca um estudante pelo nome.
    """
    nome = input("\nDigite o nome do estudante: ").strip()
    estudantes = listar_estudantes()
    encontrados = [est for est in estudantes if nome.lower() in est[1].lower()]
    
    if encontrados:
        exibir_estudantes(encontrados)
    else:
        print(f"\nNenhum estudante encontrado com o nome '{nome}'")

def ver_recomendacoes():
    """
    Exibe recomendações de carreira para um estudante.
    """
    nome = input("\nDigite o nome do estudante: ").strip()
    estudantes = listar_estudantes()
    estudante = next((est for est in estudantes if est[1].lower() == nome.lower()), None)
    
    if not estudante:
        print(f"\nEstudante '{nome}' não encontrado.")
        return
    
    # converte os dados do estudante pro formato esperado pela lógica
    dados_estudante = {
        'nome': estudante[1],
        'interesses': estudante[2] if estudante[2] else [],
        'habilidades': estudante[3] if len(estudante) > 3 and estudante[3] else [],
        'desempenho': estudante[4] if len(estudante) > 4 and estudante[4] else {}
    }
    
    # processa recomendações usando o motor 
    CAMINHO_REGRAS = os.path.join(os.path.dirname(__file__), '..', 'data', 'regras.json')
    motor = MotorDeInferencia(CAMINHO_REGRAS)
    recomendadas, proximas = motor.processa_estudante(dados_estudante)
    
    
    print("\n=== Recomendações de Carreira ===")
    
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
        
        proximas.sort(key=lambda x: x['score'], reverse=True)
        
        for c in proximas:
            print(f"\n- {c['carreira']} (score: {c['score']}%)")
            print(f"  Justificativa: {c['justificativa']}")
            print("\n  Explicação:")
            for tipo, explicacao in c['explicacao'].items():
                print(f"  - {explicacao}")
            
            
            print("\n  Sugestões para transformar em carreira recomendada:")
            for tipo, explicacao in c['explicacao'].items():
                if "Faltam" in explicacao:
                    print(f"  - {explicacao.replace('Faltam', 'Adquira')}")
    else:
        print("Nenhuma carreira próxima no momento.")

def executar_fluxo():
    """
    Executa o fluxo principal do sistema com menu interativo.
    """
    try:
        
        criar_tabela_estudantes()
        
        while True:
            opcao = exibir_menu()
            
            if opcao == "1":
                cadastrar_estudante()
            elif opcao == "2":
                estudantes = listar_estudantes()
                exibir_estudantes(estudantes)
            elif opcao == "3":
                buscar_estudante()
            elif opcao == "4":
                ver_recomendacoes()
            elif opcao == "5":
                CAMINHO_REGRAS = os.path.join(os.path.dirname(__file__), '..', 'data', 'regras.json')
                executar_menu_gestor(CAMINHO_REGRAS)
            elif opcao == "6":
                if input("\nTem certeza que deseja sair? (s/n): ").lower() == 's':
                    print("\nEncerrando o sistema...")
                    break
            else:
                print("\nOpção inválida! Por favor, escolha uma opção válida.")
    except Exception as e:
        print(f"\nErro no sistema: {str(e)}")
        print("O sistema será encerrado.") 