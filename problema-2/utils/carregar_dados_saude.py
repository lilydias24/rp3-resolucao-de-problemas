from typing import Iterator
import os.path

def carregar_dados_saude(caminho_arquivo: str) -> Iterator[str]:

    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as f:
            for linha in f:
                yield linha.strip()  # Remove espaços em branco e quebras de linha
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")

def processar_linhas(linhas: Iterator[str], quantidade: int) -> Iterator[str]:
    return (linha for i, linha in enumerate(linhas) if i < quantidade)

if __name__ == "__main__":
    caminho_arquivo = os.path.join(os.path.dirname(__file__), 'dataset_saude.csv')
    
    # Exemplo: mostrar as 3 primeiras linhas do arquivo
    dados = carregar_dados_saude(caminho_arquivo)
    for registro in processar_linhas(dados, 1):
        print(registro)