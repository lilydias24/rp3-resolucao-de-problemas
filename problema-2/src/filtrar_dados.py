import csv
from pathlib import Path
from typing import List, Dict, Callable

dir_base = Path(__file__).parent
path = dir_base.joinpath( "..", "data","dados_pacientes.csv").resolve()

head = ["Data", "Hora", "Batimentos", "Pressão Sistólica", "Pressão Diastólica", "Glicose", "Obs"]

'''
verifica se o csv existe no sistema
'''
def ler_csv(path) -> List[Dict[str, str]]:
    try:
        with open(path, "r", encoding="utf-8", newline="") as file:
            return list(csv.DictReader(file))
        
    except FileNotFoundError:
        return []

'''
verifica se o valor é inteiro através do type casting
'''
def verifica_inteiro(valor_entrada: str):
    try:
        int(valor_entrada.strip())
        return True
    except (ValueError, AttributeError):
        return False
    
    
'''
classifica os valores de entrada
'''
valores_entrada: Dict[str, Callable[[int], bool]] = {
    "Batimentos": lambda x: 60 <= x <= 100,
    "Pressão Sistólica": lambda x: x < 120,
    "Pressão Diastólica": lambda x: x < 80,
    "Glicose": lambda x: 70 <= x <= 99
}

'''
verifica se todos os dados são válidos
'''
def filtrar_entradas(registros) -> List[Dict[str, str]]:
    def nao_valido(reg: Dict[str, str]):
        return any(
            (not verifica_inteiro(reg[field])) or
            (not valores_entrada[field](int(reg[field].strip())))
            for field in valores_entrada
        )

    return list(filter(nao_valido, registros))

def segmentar_categoria(dados_segmentar):
    return {
        field: list(filter(
            lambda rec, f=field: (
                    (not verifica_inteiro(rec[f])) or
                    (not valores_entrada[f](int(rec[f].strip())))
            ),
            dados_segmentar
        ))
        for field in valores_entrada
    }


def main():
    if not path.exists():
        print("CSV não encontrado. Execute primeiro o save() para criar o arquivo.")
        return

    registros = ler_csv(path)

    fora = filtrar_entradas(registros)
    print(f"\nTotal de registros fora da faixa normal ou inválidos: {len(fora)}\n")

    segmentos = segmentar_categoria(fora)
    for campo, regs in segmentos.items():
        print(f"{campo}: {len(regs)} registro(s) fora do normal ou inválidos\n")

    '''
    exibe todos os valores anormais por categoria
    '''
    for campo, regs in segmentos.items():
        print(f"\n– {campo} ({len(regs)} registro(s) fora do normal):")
        for rec in regs:
            data = rec["Data"]
            hora = rec["Hora"]
            valor = rec[campo]
            print(f"  {data} {hora} — {campo}: {valor}")

if __name__ == "__main__":
    main()