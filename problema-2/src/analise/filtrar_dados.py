import csv
from pathlib import Path
from typing import List, Dict, Callable

dir_base = Path(__file__).parent
path = dir_base.joinpath("..", "dados", "dataset_saude.csv").resolve()

def ler_csv(path: Path) -> List[Dict[str, str]]:
    """Lê todo o CSV (ou retorna lista vazia se não existir)."""
    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))
    except Exception:
        return []

def verifica_float(valor: str) -> bool:
    """Verifica se um valor pode ser convertido para float."""
    try:
        float(valor)
        return True
    except (ValueError, TypeError):
        return False

def verifica_pressao(valor: str) -> bool:
    """Verifica se o valor da pressão arterial está no formato correto (sistólica/diastólica)."""
    try:
        if '/' not in valor:
            return False
        sistolica, diastolica = valor.split('/')
        return verifica_float(sistolica) and verifica_float(diastolica)
    except (ValueError, TypeError):
        return False

def segmentar_categoria(registros: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    """Segmenta os registros por categoria de anormalidade."""
    categorias = {
        'batimentos': [],
        'pressao': [],
        'glicose': []
    }
    
    for registro in registros:
        try:
            # Verifica batimentos
            if 'Batimentos' in registro:
                valor = registro['Batimentos'].strip()
                if valor and verifica_float(valor):
                    batimentos = float(valor)
                    if batimentos < 40 or batimentos > 200:
                        categorias['batimentos'].append(registro)

            # Verifica pressão
            if 'Pressão' in registro:
                valor = registro['Pressão'].strip()
                if valor and verifica_pressao(valor):
                    sistolica, diastolica = map(float, valor.split('/'))
                    if sistolica < 60 or sistolica > 200 or diastolica < 40 or diastolica > 120:
                        categorias['pressao'].append(registro)

            # Verifica glicose
            if 'Glicose' in registro:
                valor = registro['Glicose'].strip()
                if valor and verifica_float(valor):
                    glicose = float(valor)
                    if glicose < 40 or glicose > 400:
                        categorias['glicose'].append(registro)

        except Exception:
            continue
    
    return categorias

def main():
    if not path.exists():
        print("Arquivo dataset_saude.csv não encontrado.")
        return

    registros = ler_csv(path)
    if not registros:
        print("Nenhum registro encontrado no arquivo.")
        return

    segmentos = segmentar_categoria(registros)
    
    print("\nRegistros com valores anormais:")
    for campo, regs in segmentos.items():
        print(f"\n{campo.upper()}: {len(regs)} registro(s)")
        if regs:
            for rec in regs[:3]:  # Mostra até 3 exemplos
                if campo == 'batimentos':
                    print(f"  Data: {rec.get('Data', 'N/A')} - Batimentos: {rec.get('Batimentos', 'N/A')}")
                elif campo == 'pressao':
                    print(f"  Data: {rec.get('Data', 'N/A')} - Pressão: {rec.get('Pressão', 'N/A')}")
                elif campo == 'glicose':
                    print(f"  Data: {rec.get('Data', 'N/A')} - Glicose: {rec.get('Glicose', 'N/A')}")

if __name__ == "__main__":
    main()
