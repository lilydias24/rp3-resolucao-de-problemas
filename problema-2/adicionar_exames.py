import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict

path = Path(__file__).parent / "dados_pacientes.csv"
head = ["Data", "Hora", "Batimentos", "Pressão Sistólica", "Pressão Diastólica", "Glicose", "Obs"]


def verifica_head(path):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")

    with open(path, "r", newline="", encoding="utf-8") as file:
        linhas = list(csv.reader(file))

        if not linhas or linhas[0] != head:
            dados = linhas[1:] if len(linhas) > 1 else []

            with open(path, "w", newline="", encoding="utf-8") as wf:
                writer = csv.writer(wf)
                writer.writerow(head)
                writer.writerows(dados)


def recebe_dados() -> List[Dict[str, str]]:
    hora = datetime.now()
    base = {"Data": hora.strftime("%d/%m/%Y"), "Hora": hora.strftime("%H:%M:%S")}

    dados_header = ("Batimentos", "Pressão Sistólica", "Pressão Diastólica", "Glicose")
    entradas = {campo: input(f"Insira {campo}: ") for campo in dados_header}
    registro = {**base, **entradas, "Obs": ""}
    return [registro]


def verifica_inteiro(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False


def classifica_entrada(valor):
    bpm, sist, diast, glic = (
        map(int, (valor["Batimentos"], valor["Pressão Sistólica"], valor["Pressão Diastólica"], valor["Glicose"])))
    batimentos = "abaixo do normal" if bpm < 60 else "Normal" if bpm <= 100 else "acima do normal"

    pressao = ("Normal" if sist < 120 and diast < 80 else "Elevada" if 120 <= sist < 130 and diast < 80
                else "Hipertensão Estágio 1" if (130 <= sist < 140) or (80 <= diast < 90)
                else "Hipertensão Estágio 2")

    glicose = ("Hipoglicemia" if glic < 70 else "Normal" if glic <= 99 else "Prediabetes" if glic <= 125
                else "Diabetes")

    return "; ".join([f"Batimentos: {batimentos}", f"Pressão: {pressao}", f"Glicose: {glicose}"])


def save():
    verifica_head(path)
    registros = recebe_dados()
    campos_val = ("Batimentos", "Pressão Sistólica", "Pressão Diastólica", "Glicose")
    if not all(verifica_inteiro(valor[c]) for valor in registros for c in campos_val):
        print("Erro: todos os valores devem ser inteiros.")
        return

    registros_classificados = list(map(lambda valor: {**valor, "Obs": classifica_entrada(valor)}, registros))

    with open(path,"a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=head)
        writer.writerows(registros_classificados)

    print("Dados salvos com sucesso!")


if __name__ == "__main__":
    save()
