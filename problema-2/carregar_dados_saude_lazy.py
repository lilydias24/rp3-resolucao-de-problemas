from typing import Iterator

def carregar_dados_saude_lazy(caminho_arquivo: str) -> Iterator[str]:
    """
    Carrega os dados de saúde de forma preguiçosa a partir de um arquivo CSV.

    Args:
        caminho_arquivo (str): Caminho para o arquivo CSV.

    Returns:
        Iterator[str]: Um gerador contendo as linhas do arquivo CSV.
    """
    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as f:
            for linha in f:
                yield linha.strip()  # Remove espaços em branco e quebras de linha
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")

def processar_linhas(linhas: Iterator[str], quantidade: int) -> Iterator[str]:
    """
    Processa um número limitado de linhas de forma preguiçosa.

    Args:
        linhas (Iterator[str]): Um gerador contendo as linhas do arquivo.
        quantidade (int): Número de linhas a serem processadas.

    Returns:
        Iterator[str]: Um gerador contendo as linhas processadas.
    """
    return (linha for i, linha in enumerate(linhas) if i < quantidade)

if __name__ == "__main__":
    caminho_arquivo = r"C:\Users\eriquito\Documentos\FACUL\SEMESTRE_3\RP_III\MARCO_I\grupo-05\problema-2\dataset_saude.csv"
    
    # Exemplo: mostrar as 3 primeiras linhas do arquivo
    dados = carregar_dados_saude_lazy(caminho_arquivo)
    for registro in processar_linhas(dados, 1):
        print(registro)