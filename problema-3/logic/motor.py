"""
Motor de inferência para o sistema de recomendação de carreiras.
"""
from data.conexao import conectar

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

            explicacao = {
                'Interesse': f"Regra de Interesse: Você tem {interesses_atendidos} dos {len(interesses_necessarios)} interesses necessários. " +
                             (f"Faltam: {', '.join(interesses_faltantes)}" if interesses_faltantes else "Todos os interesses necessários foram atendidos."),
                'Habilidade': f"Regra de Habilidade: Você tem {habilidades_atendidas} das {len(habilidades_necessarias)} habilidades necessárias. " +
                              (f"Faltam: {', '.join(habilidades_faltantes)}" if habilidades_faltantes else "Todas as habilidades necessárias foram atendidas."),
                'Desempenho': f"Regra de Desempenho: Você tem {materias_atendidas} das {len(desempenho_necessario)} notas necessárias. " +
                              (f"Faltam notas adequadas em: {', '.join(materias_faltantes)}" if materias_faltantes else "Todas as notas necessárias foram atendidas.")
            }

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
            else:
                proximas.append({
                    'carreira': carreira,
                    'score': score,
                    'explicacao': explicacao,
                    'justificativa': justificativa
                })

        # Ordena por score decrescente
        recomendadas = [c for c in recomendadas if c['score'] > 0]
        proximas = [c for c in proximas if c['score'] > 0]
        recomendadas.sort(key=lambda x: x['score'], reverse=True)
        proximas.sort(key=lambda x: x['score'], reverse=True)
        return recomendadas, proximas