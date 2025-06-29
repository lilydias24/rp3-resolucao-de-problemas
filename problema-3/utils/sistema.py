"""
Módulo do fluxo principal do sistema.

Contém funções para gerenciar o fluxo de execução do sistema.
"""
<<<<<<< HEAD
from data.criar_banco import criar_tabelas
from logic.estudante import *
from logic.recomendacao import salvar_recomendacao
from logic.motor import MotorDeInferencia
from utils.exportador_csv import exportar_tendencias_para_csv
=======
import json
from data.estudante_db import criar_tabela_estudantes, salvar_estudante, listar_estudantes
from logic.logica import gerar_fatos_de_interesses, pode_seguir_carreira, carreiras_proximas
from utils.interface import (
    coletar_interesses,
    coletar_habilidades,
    coletar_desempenho_academico,
    exibir_fatos,
    exibir_estudantes
)
>>>>>>> origin/development

def exibir_menu():
    """
    Exibe o menu principal do sistema.
    """
    print("\n=== Sistema de Recomendação de Carreiras ===")
    print("1. Cadastrar novo estudante")
    print("2. Listar estudantes cadastrados")
    print("3. Buscar estudante por nome")
    print("4. Ver recomendações de carreira")
<<<<<<< HEAD
    print("5. Exportar tendências de carreira para CSV")
    print("6. Sair")
    return input("\nEscolha uma opção: ").strip()

def ver_recomendacoes():
    """
    Exibe recomendações de carreira para um estudante, buscando pelo ID.
    """
    try:
        estudantes = listar_estudantes()
        exibir_estudantes(estudantes)
        estudante_id = int(input("\nDigite o ID do estudante: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    # Buscar dados completos do estudante pelo ID
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM estudantes WHERE id = ?", (estudante_id,))
    row = cursor.fetchone()
    if not row:
        print(f"\nEstudante com ID {estudante_id} não encontrado no banco.")
        conn.close()
        return
    nome = row[0]
    conn.close()

    dados_estudante = buscar_estudante_completo_por_nome(nome)
    if not dados_estudante:
        print(f"\nEstudante '{nome}' não encontrado.")
        return

    motor = MotorDeInferencia()
    recomendadas, proximas = motor.processa_estudante(dados_estudante)

    # Salve as recomendações recomendadas
    for rec in recomendadas:
        salvar_recomendacao(estudante_id, rec['carreira'], rec['score'])

    print("\n=== Recomendações de Carreira ===")
    if recomendadas:
        print("\nCarreiras recomendadas:")
        for c in recomendadas:
            print(f"- {c['carreira']} (score: {c['score']}): {c['justificativa']}")
            for k, v in c['explicacao'].items():
                print(f"  {k}: {v}")
    else:
        print("\nNenhuma carreira específica recomendada.")

    if proximas:
        print("\nCarreiras próximas (requerem desenvolvimento adicional):")
        for c in proximas:
            print(f"- {c['carreira']} (score: {c['score']}): {c['justificativa']}")
            for k, v in c['explicacao'].items():
                print(f"  {k}: {v}")
=======
    print("5. Sair")
    return input("\nEscolha uma opção: ").strip()

def cadastrar_estudante():
    """
    Executa o fluxo de cadastro de um novo estudante.
    """
    try:
        # Coleta dados do estudante
        estudante = coletar_interesses()
        estudante = coletar_habilidades(estudante)
        estudante = coletar_desempenho_academico(estudante)
        
        # Processa os dados
        fatos = gerar_fatos_de_interesses(estudante)
        exibir_fatos(fatos)
        
        # Salva no banco
        salvar_estudante(estudante)
        print("\n Estudante cadastrado com sucesso! \n")
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
    
    # Converte os dados do estudante para o formato esperado pela lógica
    dados_estudante = {
        'nome': estudante[1],
        'interesses': estudante[2] if estudante[2] else [],
        'habilidades': estudante[3] if len(estudante) > 3 and estudante[3] else [],
        'desempenho_escolar': estudante[4] if len(estudante) > 4 and estudante[4] else {}
    }
    
    # Gera fatos e recomendações
    fatos = gerar_fatos_de_interesses(dados_estudante)
    print("\n=== Recomendações de Carreira ===")
    
    # Verifica carreiras possíveis
    carreiras_possiveis = []
    for carreira in ['desenvolvimento_software', 'data_science', 'ciencias_humanas']:
        if pode_seguir_carreira(dados_estudante, carreira):
            carreiras_possiveis.append(carreira)
    
    if carreiras_possiveis:
        print("\nCarreiras recomendadas:")
        for carreira in carreiras_possiveis:
            print(f"- {carreira.replace('_', ' ').title()}")
    else:
        print("\nNenhuma carreira específica recomendada.")
    
    # Verifica carreiras próximas
    carreiras_proximas_list = carreiras_proximas(dados_estudante)
    if carreiras_proximas_list:
        print("\nCarreiras próximas (requerem desenvolvimento adicional):")
        for carreira in carreiras_proximas_list:
            print(f"- {carreira['carreira'].replace('_', ' ').title()}")
            print(f"  Proximidade: {carreira['proximidade']:.2%}")
            print("\n  Explicação:")
            for tipo, explicacao in carreira['explicacao'].items():
                print(f"  - {explicacao}")
>>>>>>> origin/development

def executar_fluxo():
    """
    Executa o fluxo principal do sistema com menu interativo.
    """
    try:
<<<<<<< HEAD
        criar_tabelas()
        while True:
            opcao = exibir_menu()
            if opcao == "1":
                cadastrar_estudante() 
=======
        # Inicializa o banco de dados
        criar_tabela_estudantes()
        
        while True:
            opcao = exibir_menu()
            
            if opcao == "1":
                cadastrar_estudante()
>>>>>>> origin/development
            elif opcao == "2":
                estudantes = listar_estudantes()
                exibir_estudantes(estudantes)
            elif opcao == "3":
                buscar_estudante()
            elif opcao == "4":
                ver_recomendacoes()
            elif opcao == "5":
<<<<<<< HEAD
                exportar_tendencias_para_csv('reports/tendencias_carreira.csv')
            elif opcao == "6":
=======
>>>>>>> origin/development
                if input("\nTem certeza que deseja sair? (s/n): ").lower() == 's':
                    print("\nEncerrando o sistema...")
                    break
            else:
                print("\nOpção inválida! Por favor, escolha uma opção válida.")
    except Exception as e:
        print(f"\nErro no sistema: {str(e)}")
<<<<<<< HEAD
        print("O sistema será encerrado.")
=======
        print("O sistema será encerrado.") 
>>>>>>> origin/development
