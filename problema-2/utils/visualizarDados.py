from typing import Iterator, Dict
from itertools import islice
from carregar_dados_saude import carregar_dados_saude
import os.path

def processar_linhas(linhas: Iterator[str], quantidade: int) -> Iterator[str]:
    return (linha for i, linha in enumerate(linhas) if i < quantidade)

def transformar_linha_para_dict(cabecalho: str, linha: str) -> Dict[str, str]:
    """
    Transforma uma linha CSV em um dicionário usando o cabeçalho, sem usar for.
    """
    campos = list(map(str.strip, cabecalho.split(',')))  # Remove espaços extras dos campos
    valores = list(map(str.strip, linha.split(',')))  # Remove espaços extras dos valores
    
    # Garante que o número de campos e valores seja igual
    if len(campos) != len(valores):
        raise ValueError(f"Erro ao processar linha: número de campos ({len(campos)}) "
                         f"não corresponde ao número de valores ({len(valores)}).")
    
    return dict(zip(campos, valores))

def limitar_observacoes(registro: Dict[str, str]) -> Dict[str, str]:
    """
    Limita o campo "Observações" a 100 caracteres, se existir, usando map.
    """
    return dict(
        map(
            lambda item: (
                item[0],
                item[1][:100] + "..." if item[0].lower() == "observações" and len(item[1]) > 100 else item[1]
            ),
            registro.items()
        )
    )

def exibir_registro(registro: Dict[str, str]) -> None:
    """
    Exibe um único registro formatado, usando join e map.
    """
    print("-" * 50)
    print("\n".join(map(lambda item: f"{item[0]}: {item[1]}", registro.items())))
    print("-" * 50)

def visualizar_dados(dados: Iterator[str], quantidade: int) -> None:
    dados = iter(dados)  # Garante que é um iterador
    try:
        cabecalho = next(dados).strip()  # Primeira linha = Nome das colunas
    except StopIteration:
        print("O arquivo está vazio.")
        return

    registros = map(
        lambda linha: limitar_observacoes(transformar_linha_para_dict(cabecalho, linha)),
        islice(dados, quantidade)
    )

    list(map(exibir_registro, registros))  # Aplica a exibição a cada registro

if __name__ == "__main__":
    caminho_arquivo = os.path.join(os.path.dirname(__file__), '..', 'dados', 'dataset_saude.csv')
    
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
    else:
        try:
            dados = carregar_dados_saude(caminho_arquivo)
            visualizar_dados(dados, quantidade=3)  # Exibe os registros
        except Exception as e:
            print(f"Ocorreu um erro ao processar os dados: {e}")