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
        Processa o perfil do estudante e retorna as recomendações de carreiras.
        Aplica as regras lógicas para inferir as carreiras mais adequadas.
        
        Args:
            estudante (dict): Dicionário contendo o perfil do estudante
                com interesses, habilidades e desempenho escolar.
        
        Returns:
            dict: Dicionário contendo as carreiras recomendadas e próximas.
        """
        # Aplica as regras para encontrar carreiras recomendadas
        carreiras_recomendadas = []
        for carreira in CARRERAS:
            pode_seguir, pontuacao = pode_seguir_carreira(estudante, carreira)
            
            # Obtém as pontuações individuais para explicação
            _, pont_int = regra_interesse(estudante, carreira)
            _, pont_hab = regra_habilidade(estudante, carreira)
            _, pont_des = regra_desempenho(estudante, carreira)
            
            if pode_seguir:
                explicacao = {
                    'interesse': self._explica_regra(estudante, carreira, 'interesse', pont_int),
                    'habilidade': self._explica_regra(estudante, carreira, 'habilidade', pont_hab),
                    'desempenho': self._explica_regra(estudante, carreira, 'desempenho', pont_des)
                }
                carreiras_recomendadas.append((carreira, pontuacao, explicacao))
        
        # Ordena as carreiras recomendadas por pontuação
        carreiras_recomendadas.sort(key=lambda x: x[1], reverse=True)
        
        # Aplica as regras para encontrar carreiras próximas
        carreiras_proximas_list = carreiras_proximas(estudante)
        
        return {
            'carreiras_recomendadas': carreiras_recomendadas,
            'carreiras_proximas': carreiras_proximas_list
        }