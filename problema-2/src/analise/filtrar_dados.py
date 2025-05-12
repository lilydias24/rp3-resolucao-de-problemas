from typing import List, Dict, Callable
import csv
from pathlib import Path

def carregar_dados(caminho: Path) -> List[Dict[str, str]]:
    """Carrega dados de pacientes de forma funcional"""
    with caminho.open("r", encoding="utf-8") as file:
        return list(csv.DictReader(file))

def filtrar_registros(registros: List[Dict[str, str]], 
                     criterios: Dict[str, Callable[[str], bool]]) -> Dict[str, List[Dict[str, str]]]:
    """Filtra registros com abordagem funcional"""
    return {
        campo: list(filter(
            lambda reg: not criterios[campo](reg[campo]),
            registros
        ))
        for campo in criterios
    }

def obter_criterios_padrao() -> Dict[str, Callable[[str], bool]]:
    """Retorna critérios de filtragem padrão"""
    return {
        "Batimentos": lambda x: x.isdigit() and 60 <= int(x) <= 100,
        "Pressão Sistólica": lambda x: x.isdigit() and int(x) < 120,
        "Pressão Diastólica": lambda x: x.isdigit() and int(x) < 80,
        "Glicose": lambda x: x.isdigit() and 70 <= int(x) <= 99
    }

# Função principal mantida para compatibilidade
def main():
    caminho = Path(__file__).parent.parent.parent / "data" / "dados_pacientes.csv"
    if not caminho.exists():
        print("Arquivo não encontrado!")
        return

    registros = carregar_dados(caminho)
    criterios = obter_criterios_padrao()
    resultados = filtrar_registros(registros, criterios)
    
    for campo, registros in resultados.items():
        print(f"{campo}: {len(registros)} registros fora do padrão")

if __name__ == "__main__":
    main()