"""
Módulo que implementa as regras de carreira para o motor de inferência.
"""
from typing import Dict, List, Any, Set

class Regra:
    """
    Classe que representa uma regra de carreira.
    """
    def __init__(self, carreira: str, descricao: str, interesses: List[str], 
                 habilidades: List[str], desempenho: Dict[str, float]):
        """
        Inicializa uma regra de carreira.
        
        Args:
            carreira: Nome da carreira
            descricao: Descrição da carreira
            interesses: Lista de interesses necessários
            habilidades: Lista de habilidades necessárias
            desempenho: Dicionário com as notas mínimas necessárias por disciplina
        """
        self.carreira = carreira
        self.descricao = descricao
        self.interesses = set(i.lower() for i in interesses)
        self.habilidades = set(h.lower() for h in habilidades)
        self.desempenho = desempenho
    
    def avaliar(self, estudante: Dict[str, Any]) -> Dict[str, Any]:
        """
        Avalia se um estudante atende aos critérios da carreira.
        
        Args:
            estudante: Dicionário com os dados do estudante
            
        Returns:
            Dicionário com o resultado da avaliação
        """
        # Converte dados do estudante para minúsculas
        interesses_estudante = set(i.lower() for i in estudante.get('interesses', []))
        habilidades_estudante = set(h.lower() for h in estudante.get('habilidades', []))
        desempenho_estudante = estudante.get('desempenho', {})
        
        # Avalia interesses
        interesses_faltantes = self.interesses - interesses_estudante
        interesses_atendidos = len(interesses_estudante.intersection(self.interesses))
        interesses_ok = len(interesses_faltantes) == 0
        
        # Avalia habilidades
        habilidades_faltantes = self.habilidades - habilidades_estudante
        habilidades_atendidas = len(habilidades_estudante.intersection(self.habilidades))
        habilidades_ok = len(habilidades_faltantes) == 0
        
        # Avalia desempenho
        materias_faltantes = []
        materias_atendidas = 0
        desempenho_ok = True
        
        for materia, nota_min in self.desempenho.items():
            nota_estudante = desempenho_estudante.get(materia, 0)
            if nota_estudante >= nota_min:
                materias_atendidas += 1
            else:
                materias_faltantes.append(materia)
                desempenho_ok = False
        
        # Calcula score
        score = 0
        if self.interesses:
            score += (interesses_atendidos / len(self.interesses)) * 33.33
        if self.habilidades:
            score += (habilidades_atendidas / len(self.habilidades)) * 33.33
        if self.desempenho:
            score += (materias_atendidas / len(self.desempenho)) * 33.33
        
        # Gera explicações
        explicacao = {
            'interesse': f"Regra de Interesse: Você tem {interesses_atendidos} dos {len(self.interesses)} interesses necessários. " +
                        (f"Faltam: {', '.join(interesses_faltantes)}" if interesses_faltantes else "Todos os interesses necessários foram atendidos."),
            'habilidade': f"Regra de Habilidade: Você tem {habilidades_atendidas} das {len(self.habilidades)} habilidades necessárias. " +
                         (f"Faltam: {', '.join(habilidades_faltantes)}" if habilidades_faltantes else "Todas as habilidades necessárias foram atendidas."),
            'desempenho': f"Regra de Desempenho: Você tem {materias_atendidas} das {len(self.desempenho)} notas necessárias. " +
                         (f"Faltam notas adequadas em: {', '.join(materias_faltantes)}" if materias_faltantes else "Todas as notas necessárias foram atendidas.")
        }
        
        # Gera justificativa
        if interesses_ok and habilidades_ok and desempenho_ok:
            justificativa = f"Você atende a todos os critérios para a carreira de {self.carreira}."
        else:
            faltas = []
            if not interesses_ok:
                faltas.append("interesses")
            if not habilidades_ok:
                faltas.append("habilidades")
            if not desempenho_ok:
                faltas.append("desempenho acadêmico")
            justificativa = f"Você não atende aos critérios de {', '.join(faltas)} para a carreira de {self.carreira}."
        
        return {
            'recomendada': interesses_ok and habilidades_ok and desempenho_ok,
            'score': round(score, 2),
            'justificativa': justificativa,
            'explicacao': explicacao
        } 