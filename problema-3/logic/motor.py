import json
import os

estudante = {
    "interesses": ["tecnologia", "ciências"],
    "habilidades": ["programação", "resolução de problemas"],  
    "desempenho": {
        "matemática": 9,
        "física": 8,
        "português": 2
    }
}

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
        estudante (dict): Dicionário contendo os dados do estudante, incluindo interesses (list),
                          habilidades (list) e desempenho (dict de disciplina para nota).
        regras (list): Lista de regras, onde cada regra é um dicionário com as condições necessárias
                       para recomendar uma carreira.

    Returns:
        list: Lista de dicionários, cada um contendo 'carreira' e 'justificativa' para as carreiras recomendadas.
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

# Carregar regras e recomendar carreiras
regras = carregar_regras(CAMINHO_REGRAS)
sugestoes = recomendar_carreiras(estudante, regras)
for s in sugestoes:
    print(f"Carreira: {s['carreira']}\nJustificativa: {s['justificativa']}\n")

