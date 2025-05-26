import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict

dir_base = Path(__file__).parent
path = dir_base.joinpath("..", "dados", "dados_pacientes.csv").resolve()


def verifica_arquivo(path: Path):
    """Garante que o arquivo existe e tem cabeçalho."""
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        # cria arquivo vazio com cabeçalho
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Data", "Hora", "Batimentos", "Pressão", "Glicose", "Obs"])


def recebe_dados() -> List[Dict[str, str]]:
    """Lê Batimentos, Pressão e Glicose do usuário, anotando data/hora."""
    agora = datetime.now()
    base = {"Data": agora.strftime("%d/%m/%Y"), "Hora": agora.strftime("%H:%M:%S")}
    campos = ("Batimentos", "Pressão", "Glicose")
    entradas = {campo: input(f"Insira {campo}: ") for campo in campos}
    registro = {**base, **entradas, "Obs": ""}
    return [registro]


def verifica_inteiro(valor: str) -> bool:
    """Retorna True se valor puder ser convertido para int."""
    try:
        int(valor)
        return True
    except ValueError:
        return False


def classifica_entrada(valor: Dict[str, str]) -> str:
    """Classifica batimentos, pressão e glicose e monta string de observações."""
    bpm = int(valor["Batimentos"])
    pressao = int(valor["Pressão"])
    glic = int(valor["Glicose"])

    batimentos = (
        "Bradicardia" if bpm < 60 else "Normal" if bpm <= 100 else "Taquicardia"
    )

    pressao_class = (
        "Hipotensão"
        if pressao < 90
        else (
            "Normal"
            if pressao <= 120
            else "Pré-hipertensão" if pressao <= 139 else "Hipertensão"
        )
    )

    glicose = (
        "Hipoglicemia"
        if glic < 70
        else "Normal" if glic <= 99 else "Prediabetes" if glic <= 125 else "Diabetes"
    )

    return "; ".join(
        [
            f"Batimentos: {batimentos}",
            f"Pressão: {pressao_class}",
            f"Glicose: {glicose}",
        ]
    )


def save():
    verifica_arquivo(path)
    registros = recebe_dados()

    campos_num = ("Batimentos", "Pressão", "Glicose")
    if not all(verifica_inteiro(rec[c]) for rec in registros for c in campos_num):
        print("Erro: todos os valores devem ser inteiros.")
        return

    registros_classificados = [
        {**rec, "Obs": classifica_entrada(rec)} for rec in registros
    ]

    with open(path, "w", newline="", encoding="utf-8") as file:
        head = ["Data", "Hora", "Batimentos", "Pressão", "Glicose", "Obs"]
        writer = csv.DictWriter(file, fieldnames=head)
        writer.writeheader()
        writer.writerows(registros_classificados)

    print("Dados salvos com sucesso!")


if __name__ == "__main__":
    save()
