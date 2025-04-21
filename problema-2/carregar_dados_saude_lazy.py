from typing import Iterator, Dict
from csv import DictReader

def carregar_dados_saude_lazy(caminho_arquivo: str) -> Iterator[Dict[str, str]]:
    """
    Carrega os dados de saúde de forma preguiçosa a partir de um arquivo CSV.

    Args:
        caminho_arquivo (str): Caminho para o arquivo CSV.

    Returns:
        Iterator[Dict[str, str]]: Um gerador de dicionários contendo os dados de cada linha.
    """
    with open(caminho_arquivo, mode='r', encoding='utf-8') as f:
        leitor_csv = DictReader(f)
        yield from map(lambda linha: dict(linha), leitor_csv)
        
dados = carregar_dados_saude_lazy("dataset_saude.csv")

# Exemplo: mostrar os 3 primeiros registros
from itertools import islice

for registro in islice(dados, 3):
    print(registro)

