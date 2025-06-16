"""
Módulo de geração de gráficos.
"""
import os
import matplotlib.pyplot as plt
from typing import Dict, List, Any
from data.conexao import ConexaoErro
from logic.estudante import listar_estudantes
from logic.recomendacao import listar_regras
from logic.recomendacao import listar_recomendacoes

class GeradorGraficos:
    """
    Classe para geração de gráficos de desempenho e recomendações.
    """
    
    def __init__(self):
        """
        Inicializa o gerador de gráficos.
        """
        # Configura o estilo dos gráficos
        plt.style.use('default')
        
        # Cria diretórios para os gráficos
        self.base_dir = 'reports/graficos'
        self.estudantes_dir = os.path.join(self.base_dir, 'estudantes')
        self.disciplinas_dir = os.path.join(self.base_dir, 'disciplinas')
        self.recomendacoes_dir = os.path.join(self.base_dir, 'recomendacoes')
        
        os.makedirs(self.estudantes_dir, exist_ok=True)
        os.makedirs(self.disciplinas_dir, exist_ok=True)
        os.makedirs(self.recomendacoes_dir, exist_ok=True)
    
    def grafico_desempenho_disciplina(self, dados: Dict[str, float], disciplina: str) -> None:
        """
        Gera gráfico de desempenho por disciplina.
        
        Args:
            dados: Dicionário com notas dos estudantes
            disciplina: Nome da disciplina
        """
        plt.figure(figsize=(10, 6))
        plt.bar(dados.keys(), dados.values())
        plt.title(f'Desempenho em {disciplina}')
        plt.xlabel('Estudante')
        plt.ylabel('Nota')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(self.disciplinas_dir, f'desempenho_{disciplina.lower().replace(" ", "_")}.png'))
        plt.close()
    
    def grafico_desempenho_estudante(self, dados: Dict[str, float], estudante: str) -> None:
        """
        Gera gráfico de desempenho por estudante.
        
        Args:
            dados: Dicionário com notas do estudante
            estudante: Nome do estudante
        """
        plt.figure(figsize=(10, 6))
        plt.bar(dados.keys(), dados.values())
        plt.title(f'Desempenho de {estudante}')
        plt.xlabel('Disciplina')
        plt.ylabel('Nota')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(self.estudantes_dir, f'desempenho_{estudante.lower().replace(" ", "_")}.png'))
        plt.close()
    
    def grafico_recomendacoes(self, dados: List[Dict[str, Any]]) -> None:
        """
        Gera gráfico de distribuição de recomendações.
        
        Args:
            dados: Lista de dicionários com dados das recomendações
        """
        # Agrupa recomendações por carreira
        carreiras = {}
        for rec in dados:
            carreira = rec['carreira']
            if carreira not in carreiras:
                carreiras[carreira] = 0
            carreiras[carreira] += 1
        
        plt.figure(figsize=(12, 6))
        plt.pie(carreiras.values(), labels=carreiras.keys(), autopct='%1.1f%%')
        plt.title('Distribuição de Recomendações por Carreira')
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(os.path.join(self.recomendacoes_dir, 'distribuicao_recomendacoes.png'))
        plt.close()
    
    def gerar_todos_graficos(self) -> None:
        """
        Gera todos os gráficos do sistema.
        
        Raises:
            ConexaoErro: Se houver erro ao gerar os gráficos
        """
        try:
            # Obtém dados
            estudantes = listar_estudantes()
            regras = listar_regras()
            recomendacoes = listar_recomendacoes()
            
            # Gera gráficos de desempenho por disciplina
            disciplinas = set()
            for _, _, _, _, desempenho in estudantes:
                disciplinas.update(desempenho.keys())
            
            for disciplina in disciplinas:
                dados = {}
                for _, nome, _, _, desempenho in estudantes:
                    if disciplina in desempenho:
                        dados[nome] = desempenho[disciplina]
                if dados:
                    self.grafico_desempenho_disciplina(dados, disciplina)
            
            # Gera gráficos de desempenho por estudante
            for _, nome, _, _, desempenho in estudantes:
                if desempenho:
                    self.grafico_desempenho_estudante(desempenho, nome)
            
            # Gera gráfico de recomendações
            if recomendacoes:
                self.grafico_recomendacoes(recomendacoes)
            
        except Exception as e:
            raise ConexaoErro(f"Erro ao gerar gráficos: {str(e)}")

if __name__ == "__main__":
    gerador = GeradorGraficos()
    gerador.gerar_todos_graficos()