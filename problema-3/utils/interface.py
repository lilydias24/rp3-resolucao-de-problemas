"""
Módulo de interface com o usuário.

Contém funções para interação com o usuário via terminal.
"""
import json
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.estudante import Estudante
from utils.gestor_interface import DISCIPLINAS

def coletar_interesses():
    """
    Solicita ao usuário que informe seu nome e interesses e cria um objeto Estudante com esses dados.

    Returns:
        Estudante: Instância contendo nome e os interesses informados pelo usuário.
    """
    print("\n\t Cadastro de Interesses do Aluno : \n")
    nome = input("> Digite seu nome: ").strip()
    entrada = input("> Digite seus interesses, separados por vírgula (ex: artes, ciência, tecnologia):\n>> ")
    interesses = [i.strip().lower() for i in entrada.split(",") if i.strip()]
    estudante = Estudante(nome=nome, interesses=interesses)
    return estudante


def coletar_habilidades(estudante):
    """
    Solicita ao usuário que informe suas habilidades.

    Args:
        estudante (Estudante): Instância do estudante que terá suas habilidades atualizadas.

    Returns:
        Estudante: Instância atualizada com as habilidades.
    """
    print("\n\t Cadastro de Habilidades : \n")
    print("Digite suas habilidades, separadas por vírgula.")
    print("Exemplos: programação, resolução de problemas, trabalho em equipe, análise de dados")
    entrada = input(">> ").strip()
    
    habilidades = [h.strip().lower() for h in entrada.split(",") if h.strip()]
    for habilidade in habilidades:
        try:
            estudante.adicionar_habilidade(habilidade)
        except (TypeError, ValueError) as e:
            print(f"Erro ao adicionar habilidade '{habilidade}': {str(e)}")
    
    print("\n\t Habilidades registradas : \n")
    for habilidade in estudante.habilidades:
        print(f"-> {habilidade}")
    
    return estudante


def coletar_desempenho_academico(estudante):
    """
    Solicita ao usuário que informe suas notas em diferentes disciplinas.

    Args:
        estudante (Estudante): Instância do estudante que terá seu desempenho atualizado.

    Returns:
        Estudante: Instância atualizada com o desempenho acadêmico.
    """
    print("\n\t Cadastro de Desempenho Acadêmico : \n")
    print("Digite suas notas (0-10) para cada disciplina.")
    print("Digite 'fim' para sair ou deixar uma nota em branco.")
    
    desempenho = {}
    
    for disciplina in DISCIPLINAS:
        while True:
            try:
                nota = input(f"Nota em {disciplina} : ").strip().lower()
                if nota == 'fim':
                    break
                
                nota = float(nota)
                if 0 <= nota <= 10:
                    desempenho[disciplina] = nota
                    break
                else:
                    print("Por favor, digite uma nota entre 0 e 10.")
            except ValueError:
                print("Por favor, digite um número válido ou 'fim'.")
        
        if nota == 'fim':
            break
    
    estudante.desempenho_escolar = desempenho
    print("\n\t Notas: \n")
    for disciplina, nota in desempenho.items():
        print(f"-> {disciplina} : {nota}")
    
    return estudante


def exibir_fatos(fatos):
    """
    Exibe os fatos lógicos extraídos do estudante.

    Args:
        fatos (list[str]): Lista de fatos lógicos.
    """
    print("\n\t Fatos lógicos extraídos : \n")
    for fato in fatos:
        print(f"- {fato} ")


def exibir_estudantes(estudantes):
    """
    Exibe a lista de estudantes cadastrados.

    Args:
        estudantes (list[tuple]): Lista de tuplas com dados dos estudantes.
    """
    if not estudantes:
        print("\nNenhum estudante cadastrado no sistema.")
        return

    print("\n=== Estudantes Cadastrados ===")
    for est in estudantes:
        print(f"\nID: {est[0]}")
        print(f"Nome: {est[1]}")
        
        
        interesses = est[2] if est[2] else []
        print(f"Interesses: {interesses}")
        
        
        habilidades = est[3] if est[3] else []
        if habilidades:
            print(f"Habilidades: {habilidades}")
        
        
        desempenho = est[4] if est[4] else {}
        if desempenho:
            print("Desempenho Acadêmico:")
            for disciplina, nota in desempenho.items():
                print(f"  - {disciplina}: {nota}")
        
        print("-" * 40)

        dados_estudante = {
            'nome': est[1],
            'interesses': json.dumps(interesses),
            'habilidades': json.dumps(habilidades) if len(est) > 3 and est[3] else [],
            'desempenho_escolar': json.dumps(desempenho) if len(est) > 4 and est[4] else {}
        } 