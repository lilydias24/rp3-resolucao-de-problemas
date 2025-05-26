"""
Motor de inferência para o sistema de recomendação de carreiras.
"""
from logic.logica import pode_seguir_carreira, carreiras_proximas, CARRERAS, regra_interesse, regra_habilidade, regra_desempenho
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

# Merge Eric with Douglas

class MotorDeInferencia:
    """
    Motor de inferência que processa o perfil do estudante e retorna recomendações de carreiras.
    Implementa o paradigma lógico através de fatos e regras.
    """
    
    def __init__(self):
        """Inicializa o motor de inferência."""
        pass
    
    def _explica_regra(self, estudante, carreira, tipo_regra, pontuacao):
        """
        Gera uma explicação sobre como uma regra foi aplicada.
        
        Args:
            estudante (dict): Perfil do estudante
            carreira (str): Nome da carreira
            tipo_regra (str): Tipo da regra (interesse, habilidade, desempenho)
            pontuacao (float): Pontuação obtida na regra
            
        Returns:
            str: Explicação da regra
        """
        if tipo_regra == 'interesse':
            interesses_carreira = CARRERAS[carreira]['interesses']
            interesses_estudante = set(estudante['interesses'])
            interesses_faltantes = [i for i in interesses_carreira if i not in interesses_estudante]
            return f"Regra de Interesse: Você tem {len(interesses_estudante)} dos {len(interesses_carreira)} interesses necessários. " + \
                   (f"Faltam: {', '.join(interesses_faltantes)}" if interesses_faltantes else "Todos os interesses necessários foram atendidos.")
        
        elif tipo_regra == 'habilidade':
            habilidades_carreira = CARRERAS[carreira]['habilidades']
            habilidades_estudante = set(estudante['habilidades'])
            habilidades_faltantes = [h for h in habilidades_carreira if h not in habilidades_estudante]
            return f"Regra de Habilidade: Você tem {len(habilidades_estudante)} das {len(habilidades_carreira)} habilidades necessárias. " + \
                   (f"Faltam: {', '.join(habilidades_faltantes)}" if habilidades_faltantes else "Todas as habilidades necessárias foram atendidas.")
        
        elif tipo_regra == 'desempenho':
            desempenho_carreira = CARRERAS[carreira]['desempenho']
            desempenho_estudante = estudante['desempenho_escolar']
            materias_faltantes = [m for m in desempenho_carreira if m not in desempenho_estudante or desempenho_estudante[m] < 7]
            return f"Regra de Desempenho: Você tem {len(desempenho_carreira) - len(materias_faltantes)} das {len(desempenho_carreira)} notas necessárias. " + \
                   (f"Faltam notas adequadas em: {', '.join(materias_faltantes)}" if materias_faltantes else "Todas as notas necessárias foram atendidas.")
    
    def processa_estudante(self, estudante):
        """
        Processa o perfil do estudante e retorna as carreiras recomendadas e próximas.
        """
        carreiras_recomendadas = []
        lista_carreiras_proximas = []
        
        # 
        for carreira in CARRERAS:
            # verif se o estudante pode seguir a carreira
            pode_seguir, pontuacao_total = pode_seguir_carreira(estudante, carreira)
            
            if pode_seguir:
                # da as pontuações individuais para a explicação
                _, pont_int = regra_interesse(estudante, carreira)
                _, pont_hab = regra_habilidade(estudante, carreira)
                _, pont_des = regra_desempenho(estudante, carreira)
                
                # calcula o que o estudante tem e o que falta
                interesses_estudante = set(estudante['interesses'])
                interesses_carreira = set(CARRERAS[carreira]['interesses'])
                interesses_faltantes = list(interesses_carreira - interesses_estudante)
                interesses_atendidos = len(interesses_estudante.intersection(interesses_carreira))
                
                habilidades_estudante = set(estudante['habilidades'])
                habilidades_carreira = set(CARRERAS[carreira]['habilidades'])
                habilidades_faltantes = list(habilidades_carreira - habilidades_estudante)
                habilidades_atendidas = len(habilidades_estudante.intersection(habilidades_carreira))
                
                desempenho_carreira = CARRERAS[carreira]['desempenho']
                desempenho_estudante = estudante['desempenho_escolar']
                materias_faltantes = [m for m in desempenho_carreira if m not in desempenho_estudante or desempenho_estudante[m] < 7]
                materias_atendidas = len([m for m in desempenho_carreira if m in desempenho_estudante and desempenho_estudante[m] >= 7])
                
                explicacao = {
                    'interesse': f"Regra de Interesse: Você tem {interesses_atendidos} dos {len(interesses_carreira)} interesses necessários. " + \
                               (f"Faltam: {', '.join(interesses_faltantes)}" if interesses_faltantes else "Todos os interesses necessários foram atendidos."),
                    'habilidade': f"Regra de Habilidade: Você tem {habilidades_atendidas} das {len(habilidades_carreira)} habilidades necessárias. " + \
                                (f"Faltam: {', '.join(habilidades_faltantes)}" if habilidades_faltantes else "Todas as habilidades necessárias foram atendidas."),
                    'desempenho': f"Regra de Desempenho: Você tem {materias_atendidas} das {len(desempenho_carreira)} notas necessárias. " + \
                                 (f"Faltam notas adequadas em: {', '.join(materias_faltantes)}" if materias_faltantes else "Todas as notas necessárias foram atendidas.")
                }
                
                carreiras_recomendadas.append({
                    'carreira': carreira,
                    'score': pontuacao_total,
                    'explicacao': explicacao
                })
        
        # ordena as carreiras recomendadas por score
        carreiras_recomendadas.sort(key=lambda x: x['score'], reverse=True)
        
        # da as carreiras próximas
        lista_carreiras_proximas = carreiras_proximas(estudante)
        
        return {
            'carreiras_recomendadas': carreiras_recomendadas,
            'carreiras_proximas': lista_carreiras_proximas
        }