"""
Motor de inferência para o sistema de recomendação de carreiras.
"""
import json
import os

class MotorDeInferencia:
    """
    Motor de inferência que processa o perfil do estudante e retorna recomendações de carreiras.
    Lê as carreiras e critérios do arquivo regras.json, usando pesos para disciplinas.
    """

    def __init__(self, caminho_regras):
        with open(caminho_regras, encoding='utf-8') as f:
            self.regras = json.load(f)

    def processa_estudante(self, estudante):
        """
        Processa o perfil do estudante e retorna as carreiras recomendadas e próximas.
        O score de cada carreira é calculado com base nos pesos definidos para cada disciplina.
        """
        carreiras_recomendadas = []
        carreiras_proximas = []

        for regra in self.regras:
            cond = regra["condicoes"]
            pesos = cond.get("pesos", {})
            score = 0
            score_max = 0

            # interesses e habilidades: exige pelo menos um de cada
            interesses_ok = any(i.lower() in [ei.lower() for ei in estudante["interesses"]] for i in cond.get("interesses", []))
            habilidades_ok = any(h.lower() in [eh.lower() for eh in estudante["habilidades"]] for h in cond.get("habilidades", []))

            # desempenho ponderado
            desempenho_ok = True
            materias_faltantes = []
            for materia, nota_min in cond.get("desempenho", {}).items():
                peso = pesos.get(materia, 1)
                score_max += 10 * peso  # nota máxima considerada é 10
                nota_estudante = estudante["desempenho"].get(materia, 0)
                score += max(0, min(nota_estudante, 10)) * peso
                if nota_estudante < nota_min:
                    desempenho_ok = False
                    materias_faltantes.append(materia)

            # pra explicação
            interesses_carreira = set([i.lower() for i in cond.get("interesses", [])])
            interesses_estudante = set([i.lower() for i in estudante["interesses"]])
            interesses_faltantes = list(interesses_carreira - interesses_estudante)
            interesses_atendidos = len(interesses_estudante.intersection(interesses_carreira))

            habilidades_carreira = set([h.lower() for h in cond.get("habilidades", [])])
            habilidades_estudante = set([h.lower() for h in estudante["habilidades"]])
            habilidades_faltantes = list(habilidades_carreira - habilidades_estudante)
            habilidades_atendidas = len(habilidades_estudante.intersection(habilidades_carreira))

            desempenho_carreira = cond.get("desempenho", {})
            desempenho_estudante = estudante["desempenho"]
            materias_atendidas = len([m for m in desempenho_carreira if desempenho_estudante.get(m, 0) >= desempenho_carreira[m]])

            explicacao = {
                'interesse': f"Regra de Interesse: Você tem {interesses_atendidos} dos {len(interesses_carreira)} interesses necessários. " +
                             (f"Faltam: {', '.join(interesses_faltantes)}" if interesses_faltantes else "Todos os interesses necessários foram atendidos."),
                'habilidade': f"Regra de Habilidade: Você tem {habilidades_atendidas} das {len(habilidades_carreira)} habilidades necessárias. " +
                              (f"Faltam: {', '.join(habilidades_faltantes)}" if habilidades_faltantes else "Todas as habilidades necessárias foram atendidas."),
                'desempenho': f"Regra de Desempenho: Você tem {materias_atendidas} das {len(desempenho_carreira)} notas necessárias. " +
                              (f"Faltam notas adequadas em: {', '.join(materias_faltantes)}" if materias_faltantes else "Todas as notas necessárias foram atendidas.")
            }

            # carreira recomendada
            if interesses_ok and habilidades_ok and desempenho_ok:
                carreiras_recomendadas.append({
                    "carreira": regra["carreira"],
                    "score": round(score / score_max * 100, 2) if score_max > 0 else 0,
                    "justificativa": regra["justificativa"],
                    "explicacao": explicacao
                })
            # carreira próxima: falta só um dos critérios
            else:
                faltas = sum([not interesses_ok, not habilidades_ok, not desempenho_ok])
                if faltas == 1:
                    carreiras_proximas.append({
                        "carreira": regra["carreira"],
                        "score": round(score / score_max * 100, 2) if score_max > 0 else 0,
                        "justificativa": regra["justificativa"],
                        "explicacao": explicacao
                    })

        carreiras_recomendadas.sort(key=lambda x: x['score'], reverse=True)
        carreiras_proximas.sort(key=lambda x: x['score'], reverse=True)
        return carreiras_recomendadas, carreiras_proximas

def carregar_regras(caminho_regras):
    with open(caminho_regras, encoding='utf-8') as f:
        return json.load(f)

def criar_estudante(caminho_regras):
    """
    Solicita ao usuário os dados de um estudante e retorna um dicionário com essas informações,
    usando seleção numérica para evitar erros de digitação.

    Returns:
        dict: Dicionário com as chaves:
            - 'interesses' (list): áreas de interesse do estudante.
            - 'habilidades' (list): habilidades do estudante.
            - 'desempenho' (dict): disciplinas (str) e respectivas notas (float).
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Criando estudante...")
    print("Insira os dados do estudante:")

    regras = carregar_regras(caminho_regras)

    # habilidades disponíveis
    habilidades_exemplo = sorted({h for regra in regras for h in regra["condicoes"].get("habilidades", [])})
    print("Selecione suas habilidades (digite os números separados por vírgula):")
    for idx, habilidade in enumerate(habilidades_exemplo, 1):
        print(f"{idx}. {habilidade}")
    while True:
        try:
            indices = [int(i.strip()) for i in input("Números das habilidades: ").split(',')]
            habilidades_validas = [habilidades_exemplo[i-1] for i in indices if 1 <= i <= len(habilidades_exemplo)]
            if habilidades_validas:
                break
            else:
                print("Selecione pelo menos uma habilidade válida.")
        except Exception:
            print("Entrada inválida. Tente novamente.")

    # interesses disponíveis
    os.system('cls' if os.name == 'nt' else 'clear')
    interesses_exemplo = sorted({i for regra in regras for i in regra["condicoes"].get("interesses", [])})
    print("Selecione seus interesses (digite os números separados por vírgula):")
    for idx, interesse in enumerate(interesses_exemplo, 1):
        print(f"{idx}. {interesse}")
    while True:
        try:
            indices = [int(i.strip()) for i in input("Números dos interesses: ").split(',')]
            interesses_validos = [interesses_exemplo[i-1] for i in indices if 1 <= i <= len(interesses_exemplo)]
            if interesses_validos:
                break
            else:
                print("Selecione pelo menos um interesse válido.")
        except Exception:
            print("Entrada inválida. Tente novamente.")

    # disciplinas disponíveis
    disciplinas_exemplo = sorted({d for regra in regras for d in regra["condicoes"].get("desempenho", {}).keys()})
    desempenho = {}
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Informe suas notas nas disciplinas (0 a 10):")
    
    for disciplina in disciplinas_exemplo:
        while True:
            try:
                nota = float(input(f"Nota em {disciplina}: "))
                if 0 <= nota <= 10:
                    desempenho[disciplina] = nota
                    break
                else:
                    print("Nota inválida. Deve ser entre 0 e 10.")
            except ValueError:
                print("Por favor, digite um número válido.")

    return {
        "interesses": interesses_validos,
        "habilidades": habilidades_validas,
        "desempenho": desempenho
    }

