from typing import Iterator, Dict
from itertools import islice
from carregar_dados_saude import carregar_dados_saude
import os.path

def processar_linhas(linhas: Iterator[str], quantidade: int) -> Iterator[str]:
    return (linha for i, linha in enumerate(linhas) if i < quantidade)

def transformar_linha_para_dict(cabecalho: str, linha: str) -> Dict[str, str]:
    """
    Transforma uma linha CSV em um dicionário usando o cabeçalho.
    """
    campos = [campo.strip() for campo in cabecalho.split(',')]  # Remove espaços extras
    valores = [valor.strip() for valor in linha.split(',')]  # Remove espaços extras
    
    # Garante que o número de campos e valores seja igual
    if len(campos) != len(valores):
        raise ValueError(f"Erro ao processar linha: número de campos ({len(campos)}) "
                         f"não corresponde ao número de valores ({len(valores)}).")
    
    return dict(zip(campos, valores))

def visualizar_dados(dados: Iterator[str], quantidade: int) -> None:
    
    dados = iter(dados)  # Garante que é um iterador
    try:
        cabecalho = next(dados).strip()  # Primeira linha = Nome das colunas
    except StopIteration:
        print("O arquivo está vazio.")
        return
    
    registros = map(lambda linha: transformar_linha_para_dict(cabecalho, linha), islice(dados, quantidade))
    
    for registro in registros:
        print("-" * 50)
        for campo, valor in registro.items():
            if campo.lower() == "observações":  # Limita o campo "Observações" a 100 caracteres
                valor = valor[:100] + "..." if len(valor) > 100 else valor
            print(f"{campo}: {valor}")
        print("-" * 50)

if __name__ == "__main__":
    caminho_arquivo = os.path.join(os.path.dirname(__file__), 'dataset_saude.csv')
    
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
    else:
        try:
            dados = carregar_dados_saude(caminho_arquivo)
            visualizar_dados(dados, quantidade=1)  # Exibe os registros
        except Exception as e:
            print(f"Ocorreu um erro ao processar os dados: {e}")