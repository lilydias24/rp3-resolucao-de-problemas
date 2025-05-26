import csv
from pathlib import Path
from typing import List, Dict, Callable

dir_base = Path(__file__).parent
path = dir_base.joinpath("..", "data", "dados_pacientes.csv").resolve()

# novo header --> pressão
head = ["Data", "Hora", "Batimentos", "Pressão", "Glicose", "Obs"]


def ler_csv(path: Path) -> List[Dict[str, str]]:
    """Lê todo o CSV (ou retorna lista vazia se não existir)."""
    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []


def verifica_inteiro(valor_entrada: str) -> bool:
    """True se valor_entrada for um inteiro."""
    try:
        int(valor_entrada.strip())
        return True
    except (ValueError, AttributeError):
        return False



valores_entrada: Dict[str, Callable[[int], bool]] = {
    "Batimentos": lambda x: 60 <= x <= 100,
    "Pressão":    lambda x: 90 <= x <= 120,
    "Glicose":    lambda x: 70 <= x <= 99
}


def filtrar_entradas(registros: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Retorna só os registros onde algum campo:
    - não é inteiro, ou
    - está fora da faixa normal.
    """
    def invalido(rec: Dict[str, str]) -> bool:
        return any(
            (not verifica_inteiro(rec[campo])) or
            (not valores_entrada[campo](int(rec[campo].strip())))
            for campo in valores_entrada
        )
    return list(filter(invalido, registros))


def segmentar_categoria(dados: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    """
    Agrupa, por cada campo, a lista de registros inválidos ou fora da faixa.
    """
    return {
        campo: list(filter(
            lambda rec, f=campo: (
                (not verifica_inteiro(rec[f])) or
                (not valores_entrada[f](int(rec[f].strip())))
            ),
            dados
        ))
        for campo in valores_entrada
    }


def main():
    if not path.exists():
        print("CSV não encontrado. Rode primeiro o save() para gerar o arquivo com o novo cabeçalho.")
        return

    registros = ler_csv(path)
    fora = filtrar_entradas(registros)
    print(f"\nTotal de registros inválidos ou fora do normal: {len(fora)}\n")

    segmentos = segmentar_categoria(fora)
    for campo, regs in segmentos.items():
        print(f"{campo}: {len(regs)} registro(s) fora do normal\n")


    for campo, regs in segmentos.items():
        print(f"\n– {campo} ({len(regs)}):")
        for rec in regs:
            print(f"  {rec['Data']} {rec['Hora']} — {campo}: {rec[campo]}")

if __name__ == "__main__":
    main()
