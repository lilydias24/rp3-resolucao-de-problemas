"""
Módulo de interface com o usuário.

Contém funções para interação com o usuário via terminal.
"""
import json
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
    
    disciplinas = [
        "matematica", "portugues", "fisica", "quimica", "biologia",
        "historia", "geografia", "ingles", "programacao", "artes"
    ]
    
    desempenho = {}
    
    for disciplina in disciplinas:
        while True:
            try:
                opcao = input(destaque("Digite o número da habilidade (ou 0 para terminar): ")).strip()
                if opcao == "0":
                    break
                idx = int(opcao) - 1
                if 0 <= idx < len(HABILIDADES):
                    habilidade = HABILIDADES[idx]
                    if habilidade not in habilidades:
                        habilidades.append(habilidade)
                        print(sucesso(f"Habilidade '{habilidade}' adicionada!"))
                    else:
                        print(aviso(f"Habilidade '{habilidade}' já foi adicionada!"))
                else:
                    print(erro("Opção inválida!"))
            except ValueError:
                print(erro("Digite um número válido!"))
        
        # Desempenho acadêmico
        print("\n" + destaque("Digite o desempenho acadêmico do estudante:"))
        print(separador())
        print("Digite as notas para cada disciplina (0-10)")
        print("Deixe em branco para pular uma disciplina")
        print(separador())
        
        desempenho = {}
        for disciplina in DISCIPLINAS:
            while True:
                nota = input(destaque(f"{disciplina}: ")).strip()
                if not nota:
                    break
                try:
                    nota = float(nota)
                    if 0 <= nota <= 10:
                        desempenho[disciplina] = nota
                        break
                    else:
                        print(erro("A nota deve estar entre 0 e 10!"))
                except ValueError:
                    print(erro("Digite um número válido!"))
        
        return {
            'nome': nome,
            'interesses': interesses,
            'habilidades': habilidades,
            'desempenho': desempenho
        }

    @staticmethod
    def solicitar_id_regra() -> int:
        """
        Solicita o ID da regra ao usuário.
        
        Returns:
            int: ID da regra selecionada
        """
        while True:
            try:
                regra_id = int(input("\n" + destaque("Digite o ID da regra: ")).strip())
                if regra_id > 0:
                    return regra_id
                else:
                    print(erro("ID deve ser um número positivo!"))
            except ValueError:
                print(erro("Digite um número válido!"))

    @staticmethod
    def confirmar_remocao() -> bool:
        """
        Solicita confirmação para remover um item.
        
        Returns:
            bool: True se o usuário confirmou a remoção, False caso contrário
        """
        return input("\n" + destaque("Tem certeza que deseja remover? (s/n): ")).lower() == 's'

    @staticmethod
    def editar_regra(regra: Dict) -> Dict:
        """
        Solicita dados para edição de uma regra de carreira.
        
        Args:
            regra: Dicionário com os dados atuais da regra
            
        Returns:
            Dicionário com os novos dados da regra
        """
        print(f"\n{destaque('Editar Regra de Carreira')}")
        print(f"Pressione Enter para manter o valor atual entre parênteses")
        
        # Nome da carreira
        nome_atual = regra.get('carreira', '')
        nome = input(f"\nNome da carreira ({nome_atual}): ").strip()
        if not nome:
            nome = nome_atual
        
        # Justificativa
        justificativa_atual = regra.get('justificativa', '')
        justificativa = input(f"\nJustificativa ({justificativa_atual}): ").strip()
        if not justificativa:
            justificativa = justificativa_atual
        
        # Interesses
        interesses = est[2] if est[2] else []
        print(f"Interesses: {interesses}")
        
        # Habilidades
        habilidades = est[3] if est[3] else []
        if habilidades:
            print(f"Habilidades: {habilidades}")
        
        # Desempenho Escolar
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