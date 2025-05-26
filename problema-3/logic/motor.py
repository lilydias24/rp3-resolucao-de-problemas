"""
Motor de inferência para o sistema de recomendação de carreiras.
"""
from logic.logica import pode_seguir_carreira, carreiras_proximas, CARRERAS, regra_interesse, regra_habilidade, regra_desempenho

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