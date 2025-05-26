import json
import os

# estudante = {
#     "interesses": ["tecnologia", "ciências"],
#     "habilidades": ["programação", "resolução de problemas"],  
#     "desempenho": {
#         "matemática": 9,
#         "física": 8,
#         "português": 2
#     }
# }

CAMINHO_REGRAS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'regras.json'))

def carregar_regras(CAMINHO_REGRAS):
    try:
        with open(CAMINHO_REGRAS, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Arquivo de regras não encontrado: {CAMINHO_REGRAS}")
        return []
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return []
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return []
    

def recomendar_carreiras(estudante, regras):
    """
    Gera recomendações de carreiras para um estudante com base em regras fornecidas.

    Args:
        estudante (dict): Dicionário contendo os dados do estudante, incluindo:
            - 'interesses' (list): áreas de interesse do estudante.
            - 'habilidades' (list): habilidades do estudante.
            - 'desempenho' (dict): disciplinas (str) e respectivas notas (float).
        regras (list): Lista de regras, onde cada regra é um dicionário com as condições necessárias
                       para recomendar uma carreira.

    Returns:
        list: Lista de dicionários, cada um contendo 'carreira' e 'justificativa' para as carreiras recomendadas.

    Lógica:
        Para cada regra, a função verifica se o estudante atende a todos os critérios definidos:
        - Pelo menos um dos interesses do estudante deve estar presente na lista de interesses exigidos pela regra.
        - Pelo menos uma das habilidades do estudante deve estar presente na lista de habilidades exigidas pela regra.
        - Para cada disciplina exigida na regra, a nota do estudante deve ser igual ou superior ao valor mínimo definido.
        Se todas essas condições forem satisfeitas, a carreira correspondente é recomendada ao estudante.
    """
    recomendacoes = []

    for regra in regras:
        cond = regra["condicoes"]
        atende = True

        # Verificar interesses
        if not set(cond["interesses"]).intersection(estudante["interesses"]):
            atende = False
        # Verificar habilidades
        if not set(cond["habilidades"]).intersection(estudante["habilidades"]):
            atende = False
        # Verificar desempenho
        for disciplina, nota_min in cond["desempenho"].items():
            if estudante["desempenho"].get(disciplina, 0) < nota_min:
                atende = False
        
        if atende:
            recomendacoes.append({
                "carreira": regra["carreira"],
                "justificativa": regra["justificativa"]
            })

    return recomendacoes


def criar_estudante():
    """
    Solicita ao usuário os dados de um estudante e retorna um dicionário com essas informações.

    O usuário deve informar:
        - Interesses: lista de áreas de interesse, separados por vírgula.
        - Habilidades: lista de habilidades, separadas por vírgula.
        - Desempenho: pares de disciplina e nota, inseridos um a um, até digitar '1' para finalizar.

    Returns:
        dict: Dicionário com as chaves:
            - 'interesses' (list): áreas de interesse do estudante.
            - 'habilidades' (list): habilidades do estudante.
            - 'desempenho' (dict): disciplinas (str) e respectivas notas (float).
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Criando estudante...")
    print("Insira os dados do estudante:")

    # Carregar habilidades únicas das regras
    regras = carregar_regras(CAMINHO_REGRAS)
    habilidades_exemplo = set()
    for regra in regras:
        habilidades_exemplo.update(regra["condicoes"].get("habilidades", []))
    print("Lista de Habilidades:")
    for habilidade in sorted(habilidades_exemplo):
        print(f"- {habilidade}")

    # Solicitar habilidades e validar
    while True:
        habilidades = [h.strip() for h in input("Informe suas habilidades (separadas por vírgula): ").split(',')]
        habilidades_validas = [h for h in habilidades if h in habilidades_exemplo]
        if habilidades_validas:
            break
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Nenhuma habilidade válida informada. Informe pelo menos uma habilidade da lista abaixo:")
            for habilidade in sorted(habilidades_exemplo):
                print(f"- {habilidade}")

    # Informar interesses
    os.system('cls' if os.name == 'nt' else 'clear')
    interesses_exemplo = set()
    for regra in regras:
        interesses_exemplo.update(regra["condicoes"].get("interesses", []))
    print("Lista de Interesses:")
    for interesse in sorted(interesses_exemplo):
        print(f"- {interesse}")

    while True:
        interesses = [i.strip() for i in input("Informe seus interesses (separados por vírgula): ").split(',')]
        interesses_validos = [i for i in interesses if i in interesses_exemplo]
        if interesses_validos:
            break
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Nenhum interesse válido informado. Informe pelo menos um interesse da lista abaixo:")
            for interesse in sorted(interesses_exemplo):
                print(f"- {interesse}")

    # Informar disciplinas e notas
    desempenho_exemplo = set()
    for regra in regras:
        desempenho_exemplo.update(regra["condicoes"].get("desempenho", {}).keys())
    desempenho = {}
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Informe suas notas nas disciplinas. Digite '1' para finalizar.")
    print("Lista de disciplinas sugeridas:")
    for disciplina in sorted(desempenho_exemplo):
        print(f"- {disciplina}")
    while True:
        disciplina = input("Disciplina (ou '1' para finalizar): ").strip()
        if disciplina.lower() == '1':
            break
        if disciplina not in desempenho_exemplo:
            print("Disciplina não está na lista sugerida. Tente novamente.")
            continue
        try:
            nota = float(input(f"Nota em {disciplina}: "))
            while nota < 0 or nota > 10:
                print("Nota inválida. Deve ser entre 0 e 10.")
                nota = float(input(f"Nota em {disciplina}: "))
            desempenho[disciplina] = nota
        except ValueError:
            print("Nota inválida. Tente novamente.")

    return {
        "interesses": interesses_validos,
        "habilidades": habilidades_validas,
        "desempenho": desempenho
    }

# Carregar regras e recomendar carreiras
regras = carregar_regras(CAMINHO_REGRAS)
estudante = criar_estudante()
sugestoes = recomendar_carreiras(estudante, regras)
for s in sugestoes:
    print(f"Carreira: {s['carreira']}\nJustificativa: {s['justificativa']}\n")

