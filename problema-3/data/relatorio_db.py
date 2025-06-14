"""
Módulo para geração de relatórios e visualizações.
"""
import json
from data.conexao import conectar
from logic.estudante import listar_estudantes

class RelatorioDB:
    def __init__(self):
        """Inicializa o gerador de relatórios."""
        pass

    def listar_estudantes(self):
        """
        Retorna a lista de todos os estudantes cadastrados.
        
        Returns:
            list: Lista de tuplas contendo (id, nome, interesses, habilidades, desempenho)
        """
        return listar_estudantes()

    def obter_disciplinas(self):
        """
        Retorna a lista de todas as disciplinas registradas no banco.
        
        Returns:
            list: Lista de nomes de disciplinas
        """
        estudantes = listar_estudantes()
        disciplinas = set()
        
        for _, _, _, _, desempenho in estudantes:
            if desempenho:
                disciplinas.update(desempenho.keys())
        
        return sorted(list(disciplinas))

    def obter_desempenho_disciplina(self, disciplina: str):
        """
        Retorna o desempenho de todos os estudantes em uma disciplina específica.
        
        Args:
            disciplina: Nome da disciplina
            
        Returns:
            list: Lista de dicionários com dados de desempenho
        """
        estudantes = listar_estudantes()
        dados = []
        
        for _, nome, _, _, desempenho in estudantes:
            if desempenho and disciplina in desempenho:
                dados.append({
                    'estudante': nome,
                    'nota': float(desempenho[disciplina]) if desempenho[disciplina] else 0.0
                })
        
        return dados

    def obter_desempenho_estudante(self, estudante: str):
        """
        Retorna o desempenho de um estudante em todas as disciplinas.
        
        Args:
            estudante: Nome do estudante
            
        Returns:
            list: Lista de dicionários com dados de desempenho
        """
        estudantes = listar_estudantes()
        dados = []
        
        for _, nome, _, _, desempenho in estudantes:
            if nome == estudante and desempenho:
                for disciplina, nota in desempenho.items():
                    dados.append({
                        'disciplina': disciplina,
                        'nota': float(nota) if nota else 0.0
                    })
                break
        
        return dados

    def obter_recomendacoes(self):
        """
        Retorna as recomendações de carreira para todos os estudantes.
        
        Returns:
            list: Lista de dicionários com dados de recomendações
        """
        estudantes = listar_estudantes()
        dados = []
        
        for _, nome, interesses, _, _ in estudantes:
            if interesses:
                for carreira in interesses:
                    dados.append({
                        'estudante': nome,
                        'carreira': carreira
                    })
        
        return dados