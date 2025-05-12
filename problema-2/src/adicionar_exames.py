import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict

dir_base = Path(__file__).parent
path = dir_base.joinpath( "..", "data","dados_pacientes.csv").resolve()


'''
verifica se o arquivo existe no sistema
'''
def verifica_arquivo(path):
    try:
        with open(path, "r", newline="", encoding="utf-8") as file:
            header = csv.reader(file)
            return header
            
    except FileNotFoundError:
        return []


'''
recece dados do usuário fornecendo hora, data e observações dinamicamente
'''
def recebe_dados() -> List[Dict[str, str]]:
    hora = datetime.now()
    base = {"Data": hora.strftime("%d/%m/%Y"), "Hora": hora.strftime("%H:%M:%S")}

    dados_header = ("Batimentos", "Pressão Sistólica", "Pressão Diastólica", "Glicose")
    entradas = {campo: input(f"Insira {campo}: ") for campo in dados_header}
    registro = {**base, **entradas, "Obs": ""}
    return [registro]


'''
verifica se o numero é inteiro através do type casting
'''
def verifica_inteiro(input_user: str) -> bool:
    try:
        int(input_user)
        return True
    except ValueError:
        return False

'''
classifica os dados de batimentos, pressão sistólica/diastólica e glicose e adiciona os valores nas observações
'''
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


'''
salva os dados fornecidos pelo usuario no documento "dados_pacientes.csv"
'''
def save():
    verifica_arquivo(path)
    registros = recebe_dados()
    campos_val = ("Batimentos", "Pressão Sistólica", "Pressão Diastólica", "Glicose")
    if not all(verifica_inteiro(valor[c]) for valor in registros for c in campos_val):
        print("Erro: todos os valores devem ser inteiros.")
        return

    registros_classificados = list(map(lambda valor: {**valor, "Obs": classifica_entrada(valor)}, registros))

    with open(path,"w", newline="", encoding="utf-8") as file:
        head = ["Data", "Hora", "Batimentos", "Pressão Sistólica", "Pressão Diastólica", "Glicose", "Obs"]
        pen = csv.DictWriter(file, fieldnames=head)
        pen.writeheader(head)
        pen.writerows(registros_classificados)

    print("Dados salvos com sucesso!")


if __name__ == "__main__":
    save()
