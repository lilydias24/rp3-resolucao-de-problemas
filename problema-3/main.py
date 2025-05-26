"""
Sistema de recomendação de carreiras usando paradigma lógico.

Este módulo executa o fluxo principal do sistema:
- Coleta os interesses de um estudante via terminal
- Constrói os fatos lógicos a partir dos interesses
- Salva os dados no banco SQLite
- Lista os estudantes registrados
"""
from logic.logica import pode_seguir_carreira, carreiras_proximas
from models.estudante import Estudante
from logic.fato import gerar_fatos_de_interesses
from data.estudante_db import criar_tabela_estudantes, salvar_estudante, listar_estudantes


def coletar_interesses():
    """
    Solicita ao usuário que informe seu nome e interesses e cria um objeto Estudante com esses dados.

    Returns:
        Estudante: Instância contendo nome e os interesses informados pelo usuário.
    """
    print("\n Cadastro de Interesses")
    nome = input("Digite seu nome: ").strip()
    entrada = input("Digite seus interesses separados por vírgula (ex: artes, ciência, tecnologia):\n>> ")
    interesses = [i.strip().lower() for i in entrada.split(",") if i.strip()]
    estudante = Estudante(nome=nome, interesses=interesses)
    print("\n Estudante registrado :")
    print(estudante)
    return estudante


def main():
    """
    Função principal do sistema de recomendação de carreiras.

    - Executa o fluxo principal do sistema:
    - Cria a tabela no banco, se necessário
    - Coleta os interesses do estudante
    - Gera fatos lógicos a partir dos interesses
    - Salva o estudante no banco de dados
    - Exibe todos os estudantes cadastrados
    """
    criar_tabela_estudantes()
    estudante = coletar_interesses()
    fatos = gerar_fatos_de_interesses(estudante)
    
    print("\n Fatos lógicos extraídos:")
    for fato in fatos:
        print(f"- {fato}")

    salvar_estudante(estudante)
    print("\n Estudante salvo no banco de dados.")

    print("\n Estudantes salvos:")
    for est in listar_estudantes():
        print(f"ID: {est[0]} | Nome: {est[1]} | Interesses: {est[2]}")




if __name__ == "__main__":
    main()
