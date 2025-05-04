from typing import Iterator, Dict
from itertools import islice
from carregar_dados_saude import carregar_dados_saude
import os

def transformar_linha_para_dict(cabecalho: str, linha: str) -> Dict[str, str]:
    """
    Transforma uma linha CSV em um dicionário com base no cabeçalho.
    """
    campos = tuple(map(str.strip, cabecalho.split(',')))
    valores = tuple(map(str.strip, linha.split(',')))

    if len(campos) != len(valores):
        raise ValueError(
            f"Erro ao processar linha: número de campos ({len(campos)}) "
            f"não corresponde ao número de valores ({len(valores)})."
        )
    return dict(zip(campos, valores))

def limitar_observacoes(registro: Dict[str, str]) -> Dict[str, str]:
    """
    Aplica limite de 100 caracteres ao campo 'Observações'.
    """
    return {
        campo: (valor[:100] + "..." if campo.lower() == "observações" and len(valor) > 100 else valor)
        for campo, valor in registro.items()
    }

def formatar_registro(registro: Dict[str, str]) -> str:
    """
    Formata um registro para exibição legível.
    """
    return "\n".join(
        ["-" * 50] +
        [f"{campo}: {valor}" for campo, valor in registro.items()] +
        ["-" * 50]
    )

def visualizar_dados(dados: Iterator[str], quantidade: int) -> None:
    """
    Exibe os dados formatados de forma preguiçosa.
    """
    dados = iter(dados)
    try:
        cabecalho = next(dados).strip()
    except StopIteration:
        print("O arquivo está vazio.")
        return

    registros = map(
        lambda linha: limitar_observacoes(transformar_linha_para_dict(cabecalho, linha)),
        islice(dados, quantidade)
    )

    list(map(lambda reg: print(formatar_registro(reg)), registros))

if __name__ == "__main__":
    caminho_arquivo = os.path.join(os.path.dirname(__file__), 'dataset_saude.csv')

    dados = (
        carregar_dados_saude(caminho_arquivo)
        if os.path.exists(caminho_arquivo)
        else iter(print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado."))
    )

    visualizar_dados(dados, quantidade=1)
