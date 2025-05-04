from typing import Iterator
from itertools import islice
import os

def carregar_dados_saude(caminho_arquivo: str) -> Iterator[str]:
    """
    Carrega dados de saúde de forma preguiçosa a partir de um arquivo CSV.

    Args:
        caminho_arquivo: Caminho completo para o arquivo CSV.

    Returns:
        Iterator[str]: Iterador das linhas do arquivo, sem espaços ou quebras.
    """
    try:
        return map(str.strip, open(caminho_arquivo, mode='r', encoding='utf-8'))
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return iter(())
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return iter(())

def processar_linhas(linhas: Iterator[str], quantidade: int) -> Iterator[str]:
    """
    Limita a quantidade de linhas retornadas de forma preguiçosa.

    Args:
        linhas: Iterador com as linhas do arquivo.
        quantidade: Quantidade máxima de linhas a retornar.

    Returns:
        Iterator[str]: Iterador com as primeiras 'quantidade' linhas.
    """
    return islice(linhas, quantidade)

if __name__ == "__main__":
    caminho_arquivo = os.path.join(os.path.dirname(__file__), 'dataset_saude.csv')
    list(map(print, processar_linhas(carregar_dados_saude(caminho_arquivo), 1)))
