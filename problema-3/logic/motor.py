"""
Módulo do motor de inferência do sistema de recomendação de carreiras.
Responsável por processar os dados dos estudantes e gerar recomendações.
"""
from typing import Dict, List, Tuple, Any
from data.conexao import conectar, ConexaoErro
from data.transacao import executar_consulta
from logic.recomendacao import listar_regras

class MotorDeInferencia:
    """
    Classe que implementa o motor de inferência para recomendar carreiras.
    """
    def __init__(self):
        """
        Inicializa o motor de inferência.
        """
        self.conn = conectar()
        self.regras = self._carregar_regras()

    def _carregar_regras(self) -> List[Dict[str, Any]]:
        """
        Carrega as regras de recomendação do banco de dados.
        
        Returns:
            Lista de regras carregadas
            
        Raises:
            ConexaoErro: Se houver erro ao carregar regras
        """
        try:
            return listar_regras()
        except Exception as e:
            raise ConexaoErro(f"Erro ao carregar regras: {str(e)}")

    def _calcular_score(self, estudante: Dict[str, Any], regra: Dict[str, Any]) -> float:
        """
        Calcula o score de uma carreira para um estudante baseado em uma regra.
        
        Args:
            estudante: Dados do estudante
            regra: Regra de recomendação
            
        Returns:
            Score calculado (0-100)
        """
        score = 0.0
        condicoes = regra['condicoes']
        
        # Avalia interesses
        for interesse in condicoes['interesses']:
            if interesse in estudante['interesses']:
                score += 20
                
        # Avalia habilidades
        for habilidade in condicoes['habilidades']:
            if habilidade in estudante['habilidades']:
                score += 20
                
        # Avalia desempenho escolar
        for disciplina, nota_minima in condicoes['desempenho'].items():
            if disciplina in estudante['desempenho_escolar']:
                nota_estudante = estudante['desempenho_escolar'][disciplina]
                peso = condicoes['pesos'].get(disciplina, 1.0)
                if nota_estudante >= nota_minima:
                    score += 20 * peso
                
        return min(score, 100.0)

    def processa_estudante(self, estudante: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Processa os dados de um estudante e gera recomendações de carreira.
        
        Args:
            estudante: Dicionário com dados do estudante
            
        Returns:
            Tupla com (carreiras recomendadas, carreiras próximas)
            
        Raises:
            ConexaoErro: Se houver erro ao processar
        """
        try:
            # Calcula scores para cada carreira
            scores = {}
            for regra in self.regras:
                carreira = regra['carreira']
                if carreira not in scores:
                    score = self._calcular_score(estudante, regra)
                    scores[carreira] = {
                        'carreira': carreira,
                        'score': score,
                        'justificativa': regra['justificativa'],
                        'explicacao': {
                            'interesses': f"Interesses compatíveis: {', '.join(set(regra['condicoes']['interesses']) & set(estudante['interesses']))}",
                            'habilidades': f"Habilidades compatíveis: {', '.join(set(regra['condicoes']['habilidades']) & set(estudante['habilidades']))}",
                            'desempenho': f"Desempenho adequado em: {', '.join(d for d, n in regra['condicoes']['desempenho'].items() if d in estudante['desempenho_escolar'] and estudante['desempenho_escolar'][d] >= n)}"
                        }
                    }
            
            # Converte para lista e ordena por score
            scores_list = list(scores.values())
            scores_list.sort(key=lambda x: x['score'], reverse=True)
            
            # Separa em recomendadas (score >= 60) e próximas (score >= 40)
            recomendadas = [s for s in scores_list if s['score'] >= 60]
            proximas = [s for s in scores_list if 40 <= s['score'] < 60]
            
            return recomendadas, proximas
            
        except Exception as e:
            raise ConexaoErro(f"Erro ao processar estudante: {str(e)}")

    def listar_regras(self) -> List[Dict[str, Any]]:
        """
        Lista todas as regras de carreira cadastradas.
        
        Returns:
            Lista de regras cadastradas
            
        Raises:
            ConexaoErro: Se houver erro ao listar regras
        """
        try:
            return listar_regras()
        except Exception as e:
            raise ConexaoErro(f"Erro ao listar regras: {str(e)}")

    def adicionar_regra(self, regra: Dict[str, Any]) -> None:
        """
        Adiciona uma nova regra de carreira.
        
        Args:
            regra: Dicionário com os dados da regra
            
        Raises:
            ConexaoErro: Se houver erro ao adicionar regra
        """
        try:
            from logic.recomendacao import cadastrar_regra
            carreira = regra['carreira']
            criterios = regra['condicoes']
            cadastrar_regra(carreira, criterios)
            self.regras = self._carregar_regras()  # Recarrega as regras
        except Exception as e:
            raise ConexaoErro(f"Erro ao adicionar regra: {str(e)}")

    def atualizar_regra(self, regra_id: int, regra: Dict[str, Any]) -> None:
        """
        Atualiza uma regra de carreira existente.
        
        Args:
            regra_id: ID da regra a ser atualizada
            regra: Dicionário com os novos dados da regra
            
        Raises:
            ConexaoErro: Se houver erro ao atualizar regra
        """
        try:
            from logic.recomendacao import atualizar_regra
            atualizar_regra(regra_id, regra)
            self.regras = self._carregar_regras()  # Recarrega as regras
        except Exception as e:
            raise ConexaoErro(f"Erro ao atualizar regra: {str(e)}")

    def remover_regra(self, regra_id: int) -> None:
        """
        Remove uma regra de carreira.
        
        Args:
            regra_id: ID da regra a ser removida
            
        Raises:
            ConexaoErro: Se houver erro ao remover regra
        """
        try:
            from logic.recomendacao import remover_regra
            remover_regra(regra_id)
            self.regras = self._carregar_regras()  # Recarrega as regras
        except Exception as e:
            raise ConexaoErro(f"Erro ao remover regra: {str(e)}")