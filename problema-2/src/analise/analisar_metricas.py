from typing import Iterator, Dict, Callable, List
import statistics
from functools import reduce
import csv
import sys

RegistroMedico = Dict[str, str]
Metricas = Dict[str, float]

def ler_csv(caminho: str) -> List[Dict[str, str]]:
    """Lê o arquivo CSV e retorna uma lista de dicionários."""
    try:
        # Aumenta o limite de campo do CSV
        maxInt = sys.maxsize
        while True:
            try:
                csv.field_size_limit(maxInt)
                break
            except OverflowError:
                maxInt = int(maxInt/10)
        
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            # Tenta ler o arquivo com diferentes delimitadores
            for delimiter in [',', ';', '\t']:
                try:
                    arquivo.seek(0)  # Volta ao início do arquivo
                    leitor = csv.DictReader(arquivo, delimiter=delimiter)
                    registros = list(leitor)
                    if registros and len(registros[0]) > 1:  # Verifica se encontrou colunas válidas
                        return registros
                except Exception:
                    continue
            
            # Se chegou aqui, nenhum delimitador funcionou
            print("Não foi possível identificar o formato do arquivo CSV.")
            return []
            
    except Exception as e:
        print(f"Erro ao ler o arquivo: {str(e)}")
        return []

def extrair_batimentos(registros: List[Dict[str, str]]) -> List[float]:
    """Extrai os valores de batimentos dos registros."""
    try:
        return [float(reg['Batimentos Cardíacos']) for reg in registros if 'Batimentos Cardíacos' in reg]
    except (ValueError, KeyError):
        return []

def extrair_pressao(registros: List[Dict[str, str]]) -> List[float]:
    """Extrai os valores de pressão sistólica dos registros."""
    try:
        pressoes = []
        for reg in registros:
            if 'Pressão Arterial' in reg:
                sistolica = reg['Pressão Arterial'].split('/')[0]
                pressoes.append(float(sistolica))
        return pressoes
    except (ValueError, KeyError, IndexError):
        return []

def extrair_glicose(registros: List[Dict[str, str]]) -> List[float]:
    """Extrai os valores de glicose dos registros."""
    try:
        return [float(reg['Glicose']) for reg in registros if 'Glicose' in reg]
    except (ValueError, KeyError):
        return []

def calcular_metricas(valores: List[float]) -> Metricas:
    """Calcula as métricas estatísticas."""
    if not valores:
        return {}
    
    return {
        'media': statistics.mean(valores),
        'mediana': statistics.median(valores),
        'moda': statistics.mode(valores),
        'desvio_padrao': statistics.stdev(valores) if len(valores) > 1 else 0.0,
        'variancia': statistics.variance(valores) if len(valores) > 1 else 0.0
    }

def pipeline_analise(caminho: str) -> Dict[str, Metricas]:
    """Pipeline completo de análise."""
    registros = ler_csv(caminho)
    if not registros:
        return {}
    
    batimentos = extrair_batimentos(registros)
    pressoes = extrair_pressao(registros)
    glicoses = extrair_glicose(registros)
    
    return {
        'batimentos': calcular_metricas(batimentos),
        'pressao': calcular_metricas(pressoes),
        'glicose': calcular_metricas(glicoses)
    }

if __name__ == "__main__":
    caminho = "dataset_saude.csv"
    try:
        metricas = pipeline_analise(caminho)
        if not metricas:
            print("Nenhum dado válido encontrado no arquivo.")
        else:
            print("Resultado das Métricas Calculadas:")
            for tipo, valores in metricas.items():
                print(f"\n{tipo.upper()}:")
                for nome, valor in valores.items():
                    print(f"  {nome.capitalize()}: {valor:.2f}")
    except Exception as e:
        print(f"Erro inesperado na análise: {str(e)}")
