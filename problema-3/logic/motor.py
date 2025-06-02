"""
Motor de inferência para o sistema de recomendação de carreiras.
"""
from logic.logica import pode_seguir_carreira, carreiras_proximas, CARREIRAS, regra_interesse, regra_habilidade, regra_desempenho

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
    
    def processa_estudante(self, estudante):
        """
        Processa o perfil do estudante e retorna as carreiras recomendadas e próximas.
        O score de cada carreira é calculado com base nos pesos definidos para cada disciplina.
        """
        # Converte o objeto Estudante para dicionário
        dados_estudante = estudante.to_dict()
        
        carreiras_recomendadas = []
        carreiras_proximas = []

        for regra in self.regras:
            cond = regra["condicoes"]
            pesos = cond.get("pesos", {})
            score = 0
            score_max = 0

            # interesses e habilidades: exige pelo menos um de cada
            interesses_ok = any(i.lower() in [ei.lower() for ei in dados_estudante["interesses"]] for i in cond.get("interesses", []))
            habilidades_ok = any(h.lower() in [eh.lower() for eh in dados_estudante["habilidades"]] for h in cond.get("habilidades", []))

            # desempenho ponderado
            desempenho_ok = True
            materias_faltantes = []
            for materia, nota_min in cond.get("desempenho", {}).items():
                peso = pesos.get(materia, 1)
                score_max += 10 * peso  # nota máxima considerada é 10
                nota_estudante = dados_estudante["desempenho"].get(materia, 0)
                score += max(0, min(nota_estudante, 10)) * peso
                if nota_estudante < nota_min:
                    desempenho_ok = False
                    materias_faltantes.append(materia)

            # pra explicação
            interesses_carreira = set([i.lower() for i in cond.get("interesses", [])])
            interesses_estudante = set([i.lower() for i in dados_estudante["interesses"]])
            interesses_faltantes = list(interesses_carreira - interesses_estudante)
            interesses_atendidos = len(interesses_estudante.intersection(interesses_carreira))

            habilidades_carreira = set([h.lower() for h in cond.get("habilidades", [])])
            habilidades_estudante = set([h.lower() for h in dados_estudante["habilidades"]])
            habilidades_faltantes = list(habilidades_carreira - habilidades_estudante)
            habilidades_atendidas = len(habilidades_estudante.intersection(habilidades_carreira))

            desempenho_carreira = cond.get("desempenho", {})
            desempenho_estudante = dados_estudante["desempenho"]
            materias_atendidas = len([m for m in desempenho_carreira if desempenho_estudante.get(m, 0) >= desempenho_carreira[m]])

            # ... existing code ...