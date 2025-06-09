"""
Módulo principal do sistema de recomendação de carreiras.

Contém a classe Sistema que gerencia todas as funcionalidades do sistema, incluindo:
- Menus e interfaces
- Gerenciamento de estudantes
- Geração de relatórios
- Recomendações de carreiras
"""
import os
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

def exibir_menu():
    """
    Exibe o menu principal do sistema.
    """
    print("\n=== Sistema de Recomendação de Carreiras ===")
    print("1. Cadastrar novo estudante")
    print("2. Listar estudantes cadastrados")
    print("3. Buscar estudante por nome")
    print("4. Ver recomendações de carreira")
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
        
        # Salva no banco
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
    
    # Converte os dados do estudante para o formato esperado pela lógica
    dados_estudante = {
        'nome': estudante[1],
        'interesses': estudante[2] if estudante[2] else [],
        'habilidades': estudante[3] if len(estudante) > 3 and estudante[3] else [],
        'desempenho': estudante[4] if len(estudante) > 4 and estudante[4] else {}
    }
    
    # Processa recomendações usando o motor de inferência
    CAMINHO_REGRAS = os.path.join(os.path.dirname(__file__), '..', 'data', 'regras.json')
    motor = MotorDeInferencia(CAMINHO_REGRAS)
    recomendadas, proximas = motor.processa_estudante(dados_estudante)
    
    # Exibe as recomendações
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

def executar_fluxo():
    """
    Executa o fluxo principal do sistema com menu interativo.
    """
    try:
        # Inicializa o banco de dados
        criar_tabela_estudantes()
        
        while True:
            self.exibir_menu_principal()
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                self.cadastrar_estudante()
            elif opcao == "2":
                self.listar_todos_estudantes()
            elif opcao == "3":
                self.excluir_estudante_sistema()
            elif opcao == "4":
                self.gerar_relatorios()
            elif opcao == "0":
                print("\nSaindo do sistema...")
                break
            else:
                print("\nOpção inválida!")
            
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    sistema = Sistema()
    sistema.executar()