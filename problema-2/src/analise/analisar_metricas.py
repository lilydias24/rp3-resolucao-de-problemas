from typing import Iterator, Dict, List, Tuple, Callable
import statistics
from functools import reduce
from carregar_dados_saude_lazy import carregar_dados_saude_lazy

Registro = Dict[str, str]
Metricas = Dict[str, float]

def converter_registros(registros: Iterator[str]) -> Iterator[Registro]:
    """
    Converte linhas de CSV para dicionários de registros médicos.
    Ignora linhas inválidas.
    
    Args:
        registros: Iterador de strings no formato CSV
        
    Returns:
        Iterador de dicionários com os dados parseados
        
    Example:
        >>> linhas = ["data,valor", "2023-01-01,72"]
        >>> next(converter_registros(linhas))
        {'data': '2023-01-01', 'valor': '72'}
    """
    for linha in registros:
        if not linha.strip() or linha.startswith('data,'):
            continue
        partes = linha.split(',')
        if len(partes) != 2:
            continue  
        yield {'data': partes[0], 'valor': partes[1]}

def extrair_valores_numericos(registros: Iterator[Registro]) -> Iterator[float]:
    """
    Extrai e converte valores numéricos dos registros.
    
    Args:
        registros: Iterador de dicionários contendo campo 'valor'
        
    Returns:
        Iterador de valores convertidos para float
        
    Raises:
        ValueError: Se encontrar valor não numérico
        
    Example:
        >>> registros = [{'valor': '72'}, {'valor': '75.5'}]
        >>> list(extrair_valores_numericos(registros))
        [72.0, 75.5]
    """
    for reg in registros:
        try:
            yield float(reg['valor'])
        except (KeyError, ValueError):
            continue

def calcular_metricas(valores: Iterator[float]) -> Metricas:
    """
    Calcula métricas estatísticas sobre os valores.
    
    Args:
        valores: Iterador de valores numéricos
        
    Returns:
        Dicionário com as métricas calculadas:
        - media: Média aritmética
        - mediana: Valor central
        - moda: Valor mais frequente
        - desvio_padrao: Dispersão dos dados
        - variancia: Quadrado do desvio padrão
        
    Example:
        >>> calcular_metricas([70, 72, 72, 76])
        {'media': 72.5, 'mediana': 72.0, 'moda': 72, ...}
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
    """
    Pipeline completo para análise de dados médicos.
    
    Args:
        caminho_arquivo: Caminho para o arquivo CSV
        
    Returns:
        Métricas calculadas sobre os dados
        
    Example:
        >>> pipeline_analise("dados/batimentos.csv")
        {'media': 72.5, 'mediana': 72.0, ...}
    """
    return aplicar_pipeline(
        carregar_dados_saude_lazy(caminho_arquivo),
        converter_registros,
        extrair_valores_numericos,
        calcular_metricas
    )

def aplicar_pipeline(data: Iterator, *funcs: Callable) -> Metricas:
    """Aplica uma sequência de funções nos dados."""
    return reduce(lambda x, f: f(x), funcs, data)

if __name__ == "__main__":
    caminho = "batimentos.csv"
    try:
        metricas = pipeline_analise(caminho)
        print("Resultado das Métricas Calculadas:")
        for nome, valor in metricas.items():
            print(f"{nome.capitalize()}: {valor:.2f}")
    except FileNotFoundError:
        print(f"Erro: Arquivo {caminho} não encontrado")
    except Exception as e:
        print(f"Erro na análise: {str(e)}")