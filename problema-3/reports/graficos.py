"""
Módulo para geração de gráficos de desempenho acadêmico.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List, Dict
import os

class GeradorGraficos:
    def __init__(self, diretorio_saida: str = "reports/graficos"):
        """
        Inicializa o gerador de gráficos.
        
        Args:
            diretorio_saida: Diretório onde os gráficos serão salvos
        """
        self.diretorio_saida = diretorio_saida
        os.makedirs(diretorio_saida, exist_ok=True)
        
    def grafico_desempenho_disciplina(self, dados: List[Dict], disciplina: str):
        """
        Gera gráfico de desempenho por disciplina.
        
        Args:
            dados: Lista de dicionários com dados de desempenho
            disciplina: Nome da disciplina
        """
        df = pd.DataFrame(dados)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x='estudante', y='nota')
        plt.title(f'Desempenho em {disciplina}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        caminho_arquivo = os.path.join(self.diretorio_saida, f'desempenho_{disciplina.lower()}.png')
        plt.savefig(caminho_arquivo)
        plt.close()
        
    def grafico_desempenho_estudante(self, dados: List[Dict], estudante: str):
        """
        Gera gráfico de desempenho por estudante.
        
        Args:
            dados: Lista de dicionários com dados de desempenho
            estudante: Nome do estudante
        """
        df = pd.DataFrame(dados)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x='disciplina', y='nota')
        plt.title(f'Desempenho do Estudante {estudante}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        caminho_arquivo = os.path.join(self.diretorio_saida, f'desempenho_{estudante.lower()}.png')
        plt.savefig(caminho_arquivo)
        plt.close()
        
    def grafico_recomendacoes(self, dados: List[Dict]):
        """
        Gera gráfico de distribuição de recomendações.
        
        Args:
            dados: Lista de dicionários com dados de recomendações
        """
        df = pd.DataFrame(dados)
        
        plt.figure(figsize=(12, 6))
        sns.countplot(data=df, x='carreira')
        plt.title('Distribuição de Recomendações de Carreira')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        caminho_arquivo = os.path.join(self.diretorio_saida, 'distribuicao_recomendacoes.png')
        plt.savefig(caminho_arquivo)
        plt.close()