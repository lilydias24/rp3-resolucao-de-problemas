"""
Motor de inferência para o sistema de recomendação de carreiras.
"""
<<<<<<< HEAD
from data.conexao import conectar
=======
from logic.logica import pode_seguir_carreira, carreiras_proximas, CARREIRAS, regra_interesse, regra_habilidade, regra_desempenho
>>>>>>> origin/development

class MotorDeInferencia:
    """
    Motor de inferência que processa o perfil do estudante e retorna recomendações de carreiras.
<<<<<<< HEAD
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

=======
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
            interesses_carreira = CARREIRAS[carreira]['interesses']
            interesses_estudante = set(estudante['interesses'])
            interesses_faltantes = [i for i in interesses_carreira if i not in interesses_estudante]
            return f"Regra de Interesse: Você tem {len(interesses_estudante)} dos {len(interesses_carreira)} interesses necessários. " + \
                   (f"Faltam: {', '.join(interesses_faltantes)}" if interesses_faltantes else "Todos os interesses necessários foram atendidos.")
        
        elif tipo_regra == 'habilidade':
            habilidades_carreira = CARREIRAS[carreira]['habilidades']
            habilidades_estudante = set(estudante['habilidades'])
            habilidades_faltantes = [h for h in habilidades_carreira if h not in habilidades_estudante]
            return f"Regra de Habilidade: Você tem {len(habilidades_estudante)} das {len(habilidades_carreira)} habilidades necessárias. " + \
                   (f"Faltam: {', '.join(habilidades_faltantes)}" if habilidades_faltantes else "Todas as habilidades necessárias foram atendidas.")
        
        elif tipo_regra == 'desempenho':
            desempenho_carreira = CARREIRAS[carreira]['desempenho']
            desempenho_estudante = estudante['desempenho_escolar']
            materias_faltantes = [m for m in desempenho_carreira if m not in desempenho_estudante or desempenho_estudante[m] < 7]
            return f"Regra de Desempenho: Você tem {len(desempenho_carreira) - len(materias_faltantes)} das {len(desempenho_carreira)} notas necessárias. " + \
                   (f"Faltam notas adequadas em: {', '.join(materias_faltantes)}" if materias_faltantes else "Todas as notas necessárias foram atendidas.")
    
>>>>>>> origin/development
    def processa_estudante(self, estudante):
        """
        Processa o perfil do estudante e retorna as carreiras recomendadas e próximas.
        """
<<<<<<< HEAD
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
=======
        carreiras_recomendadas = []
        lista_carreiras_proximas = []
        
        
        for carreira in CARREIRAS:
            # verif se o estudante pode seguir a carreira
            pode_seguir, pontuacao_total = pode_seguir_carreira(estudante, carreira)
            
            if pode_seguir:
                # da as pontuações individuais para a explicação
                _, pont_int = regra_interesse(estudante, carreira)
                _, pont_hab = regra_habilidade(estudante, carreira)
                _, pont_des = regra_desempenho(estudante, carreira)
                
                # calcula o que o estudante tem e o que falta
                interesses_estudante = set(estudante['interesses'])
                interesses_carreira = set(CARREIRAS[carreira]['interesses'])
                interesses_faltantes = list(interesses_carreira - interesses_estudante)
                interesses_atendidos = len(interesses_estudante.intersection(interesses_carreira))
                
                habilidades_estudante = set(estudante['habilidades'])
                habilidades_carreira = set(CARREIRAS[carreira]['habilidades'])
                habilidades_faltantes = list(habilidades_carreira - habilidades_estudante)
                habilidades_atendidas = len(habilidades_estudante.intersection(habilidades_carreira))
                
                desempenho_carreira = CARREIRAS[carreira]['desempenho']
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
>>>>>>> origin/development
