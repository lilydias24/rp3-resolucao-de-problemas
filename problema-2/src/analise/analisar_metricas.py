from typing import Iterator, Dict, Callable
import statistics
from functools import reduce
from .carregar_dados_saude import carregar_dados_saude
from itertools import starmap

RegistroMedico = Dict[str, str]
Metricas = Dict[str, float]

def linha_valida(linha: str) -> bool:
    return linha.strip() != "" and not linha.startswith('data,') and linha.count(',') == 1

def dividir_linha_em_registro(linha: str) -> RegistroMedico:
    partes = linha.split(',')
    return {'data': partes[0], 'valor': partes[1]}

def converter_registros(registros: Iterator[str]) -> Iterator[RegistroMedico]:
    """
    Converte apenas as linhas válidas usando map/filter (sem `for`).
    """
    return map(dividir_linha_em_registro, filter(linha_valida, registros))

def is_float(valor: str) -> bool:
    try:
        float(valor)
        return True
    except ValueError:
        return False

def extrair_valores_numericos(registros: Iterator[RegistroMedico]) -> Iterator[float]:
    """
    Extrai apenas os valores que são realmente convertíveis em float.
    """
    return map(lambda reg: float(reg['valor']),
               filter(lambda reg: 'valor' in reg and is_float(reg['valor']), registros))

def calcular_metricas(valores: Iterator[float]) -> Metricas:
    """
    Converte o iterador em lista e aplica estatísticas puramente funcionais.
    """
    valores_lista = list(valores)
    if not valores_lista:
        return {}
    
    return {
        'media': statistics.mean(valores_lista),
        'mediana': statistics.median(valores_lista),
        'moda': statistics.mode(valores_lista),
        'desvio_padrao': statistics.stdev(valores_lista) if len(valores_lista) > 1 else 0.0,
        'variancia': statistics.variance(valores_lista) if len(valores_lista) > 1 else 0.0
    }

def pipeline_analise(caminho_arquivo: str) -> Metricas:
    return aplicar_pipeline(
        carregar_dados_saude(caminho_arquivo),
        converter_registros,
        extrair_valores_numericos,
        calcular_metricas
    )

def aplicar_pipeline(data: Iterator, *funcs: Callable) -> Metricas:
    return reduce(lambda acc, f: f(acc), funcs, data)

if __name__ == "__main__":
    caminho = "batimentos.csv"
    try:
        metricas = pipeline_analise(caminho)
        if not metricas:
            print("Nenhum dado válido encontrado no arquivo.")
        else:
            print("Resultado das Métricas Calculadas:")
            for nome, valor in metricas.items():
                print(f"{nome.capitalize()}: {valor:.2f}")
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho}' não encontrado.")
    except Exception as e:
        print(f"Erro inesperado na análise: {str(e)}")
