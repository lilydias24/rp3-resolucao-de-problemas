"""
Módulo para geração de gráficos de desempenho acadêmico.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List, Dict
import os
import re

class GeradorGraficos:
    def __init__(self, diretorio_saida: str = "reports/graficos"):
        """
        Inicializa o gerador de gráficos.

        Args:
            diretorio_saida: Diretório onde os gráficos serão salvos
        """
        self.diretorio_saida = diretorio_saida
        os.makedirs(diretorio_saida, exist_ok=True)

    def _sanitizar_nome(self, nome: str) -> str:
        """
        Remove caracteres especiais de nomes de arquivos.
        """
        return re.sub(r'[^a-zA-Z0-9_-]', '_', nome.lower())

    def grafico_desempenho_disciplina(self, dados: List[Dict], disciplina: str):
        """
        Gera gráfico de desempenho por disciplina.

        Args:
            dados: Lista de dicionários com dados de desempenho
            disciplina: Nome da disciplina
        """
        if not dados:
            print("Nenhum dado fornecido para gerar o gráfico de disciplina.")
            return

        df = pd.DataFrame(dados)

        if 'estudante' not in df.columns or 'nota' not in df.columns:
            print("Colunas esperadas ('estudante' e 'nota') ausentes.")
            return

        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x='estudante', y='nota')
        plt.title(f'Desempenho em {disciplina}')
        plt.xticks(rotation=45)
        plt.tight_layout()

        nome_arquivo = self._sanitizar_nome(disciplina)
        caminho_arquivo = os.path.join(self.diretorio_saida, f'desempenho_{nome_arquivo}.png')
        try:
            plt.savefig(caminho_arquivo)
        except Exception as e:
            print(f"Erro ao salvar o gráfico: {e}")
        plt.close()

    def grafico_desempenho_estudante(self, dados: List[Dict], estudante: str):
        """
        Gera gráfico de desempenho por estudante.

        Args:
            dados: Lista de dicionários com dados de desempenho
            estudante: Nome do estudante
        """
        if not dados:
            print("Nenhum dado fornecido para gerar o gráfico do estudante.")
            return

        df = pd.DataFrame(dados)

        if 'disciplina' not in df.columns or 'nota' not in df.columns:
            print("Colunas esperadas ('disciplina' e 'nota') ausentes.")
            return

        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x='disciplina', y='nota')
        plt.title(f'Desempenho do Estudante {estudante}')
        plt.xticks(rotation=45)
        plt.tight_layout()

        nome_arquivo = self._sanitizar_nome(estudante)
        caminho_arquivo = os.path.join(self.diretorio_saida, f'desempenho_{nome_arquivo}.png')
        try:
            plt.savefig(caminho_arquivo)
        except Exception as e:
            print(f"Erro ao salvar o gráfico: {e}")
        plt.close()

    def grafico_recomendacoes(self, dados: List[Dict]):
        """
        Gera gráfico de distribuição de recomendações.

        Args:
            dados: Lista de dicionários com dados de recomendações
        """
        if not dados:
            print("Nenhum dado fornecido para gerar o gráfico de recomendações.")
            return

        df = pd.DataFrame(dados)

        if 'carreira' not in df.columns:
            print("Coluna esperada ('carreira') ausente.")
            return

        plt.figure(figsize=(12, 6))
        sns.countplot(data=df, x='carreira')
        plt.title('Distribuição de Recomendações de Carreira')
        plt.xticks(rotation=45)
        plt.tight_layout()

        caminho_arquivo = os.path.join(self.diretorio_saida, 'distribuicao_recomendacoes.png')
        try:
            plt.savefig(caminho_arquivo)
        except Exception as e:
            print(f"Erro ao salvar o gráfico: {e}")
        plt.close()
