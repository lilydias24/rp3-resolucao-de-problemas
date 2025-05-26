"""
Módulo de interface com o usuário.

Contém funções para interação com o usuário via terminal.
"""
from models.estudante import Estudante

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
    
    disciplinas = [
        "matematica", "portugues", "fisica", "quimica", "biologia",
        "historia", "geografia", "ingles", "programacao", "artes"
    ]
    
    print("\n\t Desempenho acadêmico: \n")
    desempenho = {}
    
    for disciplina in disciplinas:
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
    print("\n\t Estudantes salvos: \n")
    for est in estudantes:
        print(f"ID: {est[0]} | Nome: {est[1]} | Interesses: {est[2]}") 