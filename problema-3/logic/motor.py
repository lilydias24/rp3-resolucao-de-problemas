"""
Motor de inferência para o sistema de recomendação de carreiras.
"""
<<<<<<< HEAD
import json
import os
from typing import Dict, List, Any, Tuple
from utils.gestor_interface import DISCIPLINAS, INTERESSES, HABILIDADES, selecionar_opcoes

def criar_estudante(caminho_regras: str) -> Dict[str, Any]:
    """
    Cria um estudante a partir da entrada do usuário.
    
    Args:
        caminho_regras: Caminho para o arquivo de regras
        
    Returns:
        Dicionário com os dados do estudante
    """
    print("\n=== Cadastro de Estudante ===")
    
    nome = input("\nNome do estudante: ").strip()
    while not nome:
        print("O nome não pode estar vazio!")
        nome = input("Nome do estudante: ").strip()
    
    interesses = selecionar_opcoes(INTERESSES, "Selecione seus Interesses")
    while not interesses:
        print("Você deve selecionar pelo menos um interesse!")
        interesses = selecionar_opcoes(INTERESSES, "Selecione seus Interesses")
    
    habilidades = selecionar_opcoes(HABILIDADES, "Selecione suas Habilidades")
    while not habilidades:
        print("Você deve selecionar pelo menos uma habilidade!")
        habilidades = selecionar_opcoes(HABILIDADES, "Selecione suas Habilidades")
    
    print("\nInforme suas notas nas disciplinas (0 a 10):")
    notas = {}
    for disciplina in DISCIPLINAS:
        while True:
            try:
                nota = float(input(f"Nota em {disciplina}: "))
                if 0 <= nota <= 10:
                    notas[disciplina] = nota
                    break
                else:
                    print("A nota deve estar entre 0 e 10!")
            except ValueError:
                print("Por favor, digite um número válido!")
    
    return {
        "nome": nome,
        "interesses": interesses,
        "habilidades": habilidades,
        "notas": notas
    }
=======
from data.conexao import conectar
>>>>>>> eric-branch

class MotorDeInferencia:
    """
    Motor de inferência que processa o perfil do estudante e retorna recomendações de carreiras.
    Agora busca as regras diretamente do banco de dados.
    """

    def __init__(self):
        pass

    def _buscar_regras_do_banco(self):
        """
        Busca todas as regras de carreira e seus relacionamentos do banco de dados.
        Retorna uma lista de dicionários, um para cada carreira.
        """
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, carreira, justificativa FROM regras_carreira")
        regras = []
        for regra_id, carreira, justificativa in cursor.fetchall():
            # Interesses
            cursor.execute("""
                SELECT i.interesse FROM interesses_regra ir
                JOIN interesses i ON ir.interesse_id = i.id
                WHERE ir.regra_id = ?
            """, (regra_id,))
            interesses = [row[0] for row in cursor.fetchall()]
            # Habilidades
            cursor.execute("""
                SELECT h.habilidade FROM habilidades_regra hr
                JOIN habilidades h ON hr.habilidade_id = h.id
                WHERE hr.regra_id = ?
            """, (regra_id,))
            habilidades = [row[0] for row in cursor.fetchall()]
            # Desempenho
            cursor.execute("""
                SELECT d.disciplina, dr.nota_min, dr.peso FROM desempenho_regra dr
                JOIN disciplinas d ON dr.disciplina_id = d.id
                WHERE dr.regra_id = ?
            """, (regra_id,))
            desempenho = {row[0]: {'nota_min': row[1], 'peso': row[2]} for row in cursor.fetchall()}

            regras.append({
                'carreira': carreira,
                'justificativa': justificativa,
                'interesses': interesses,
                'habilidades': habilidades,
                'desempenho': desempenho
            })
        conn.close()
        return regras

    def processa_estudante(self, estudante):
        """
        Processa o perfil do estudante e retorna as carreiras recomendadas e próximas.
        """
        regras = self._buscar_regras_do_banco()
        recomendadas = []
        proximas = []

        for regra in regras:
            carreira = regra['carreira']
            justificativa = regra['justificativa']
            interesses_necessarios = set(regra['interesses'])
            habilidades_necessarias = set(regra['habilidades'])
            desempenho_necessario = regra['desempenho']

<<<<<<< HEAD
            # interesses e habilidades: exige pelo menos um de cada
            interesses_ok = any(i.lower() in [ei.lower() for ei in estudante["interesses"]] for i in cond.get("interesses", []))
            habilidades_ok = any(h.lower() in [eh.lower() for eh in estudante["habilidades"]] for h in cond.get("habilidades", []))

            # desempenho ponderado
            desempenho_ok = True
            materias_faltantes = []
            for materia, nota_min in cond.get("desempenho", {}).items():
                peso = pesos.get(materia, 1)
                score_max += 10 * peso  # nota máxima considerada é 10
                nota_estudante = estudante["notas"].get(materia, 0)
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
            desempenho_estudante = estudante["notas"]
            materias_atendidas = len([m for m in desempenho_carreira if desempenho_estudante.get(m, 0) >= desempenho_carreira[m]])

=======
            interesses_estudante = set(estudante['interesses'])
            habilidades_estudante = set(estudante['habilidades'])
            desempenho_estudante = estudante['desempenho_escolar']

            # Interesses
            interesses_faltantes = list(interesses_necessarios - interesses_estudante)
            interesses_atendidos = len(interesses_estudante & interesses_necessarios)

            # Habilidades
            habilidades_faltantes = list(habilidades_necessarias - habilidades_estudante)
            habilidades_atendidas = len(habilidades_estudante & habilidades_necessarias)

            # Desempenho
            materias_faltantes = []
            materias_atendidas = 0
            for materia, info in desempenho_necessario.items():
                nota_min = info['nota_min']
                if materia in desempenho_estudante and desempenho_estudante[materia] >= nota_min:
                    materias_atendidas += 1
                else:
                    materias_faltantes.append(materia)

>>>>>>> eric-branch
            explicacao = {
                'Interesse': f"Regra de Interesse: Você tem {interesses_atendidos} dos {len(interesses_necessarios)} interesses necessários. " +
                             (f"Faltam: {', '.join(interesses_faltantes)}" if interesses_faltantes else "Todos os interesses necessários foram atendidos."),
                'Habilidade': f"Regra de Habilidade: Você tem {habilidades_atendidas} das {len(habilidades_necessarias)} habilidades necessárias. " +
                              (f"Faltam: {', '.join(habilidades_faltantes)}" if habilidades_faltantes else "Todas as habilidades necessárias foram atendidas."),
                'Desempenho': f"Regra de Desempenho: Você tem {materias_atendidas} das {len(desempenho_necessario)} notas necessárias. " +
                              (f"Faltam notas adequadas em: {', '.join(materias_faltantes)}" if materias_faltantes else "Todas as notas necessárias foram atendidas.")
            }

<<<<<<< HEAD
            # carreira recomendada
            if interesses_ok and habilidades_ok and desempenho_ok:
                carreiras_recomendadas.append({
                    "carreira": regra["carreira"],
                    "score": round(score / score_max * 100, 2) if score_max > 0 else 0,
                    "justificativa": regra["justificativa"],
                    "explicacao": explicacao
                })
            # carreira próxima: falta só um dos critérios
=======
            # Score simples: soma dos percentuais de cada critério
            score = 0
            total_criterios = 3
            if len(interesses_necessarios) > 0:
                score += interesses_atendidos / len(interesses_necessarios)
            else:
                total_criterios -= 1
            if len(habilidades_necessarias) > 0:
                score += habilidades_atendidas / len(habilidades_necessarias)
            else:
                total_criterios -= 1
            if len(desempenho_necessario) > 0:
                score += materias_atendidas / len(desempenho_necessario)
            else:
                total_criterios -= 1
            score = round((score / total_criterios) * 100, 2) if total_criterios > 0 else 0

            # Critério para recomendar: todos os critérios atendidos
            if not interesses_faltantes and not habilidades_faltantes and not materias_faltantes:
                recomendadas.append({
                    'carreira': carreira,
                    'score': score,
                    'explicacao': explicacao,
                    'justificativa': justificativa
                })
>>>>>>> eric-branch
            else:
                proximas.append({
                    'carreira': carreira,
                    'score': score,
                    'explicacao': explicacao,
                    'justificativa': justificativa
                })

<<<<<<< HEAD
        carreiras_recomendadas.sort(key=lambda x: x['score'], reverse=True)
        carreiras_proximas.sort(key=lambda x: x['score'], reverse=True)
        return carreiras_recomendadas, carreiras_proximas

def carregar_regras(caminho_regras):
    with open(caminho_regras, encoding='utf-8') as f:
        return json.load(f)

=======
        # Ordena por score decrescente
        recomendadas = [c for c in recomendadas if c['score'] > 0]
        proximas = [c for c in proximas if c['score'] > 0]
        recomendadas.sort(key=lambda x: x['score'], reverse=True)
        proximas.sort(key=lambda x: x['score'], reverse=True)
        return recomendadas, proximas
>>>>>>> eric-branch
