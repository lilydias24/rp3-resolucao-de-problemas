from pathlib import Path
from datetime import datetime
from typing import Dict, List
import csv

# Configuração de caminhos
CAMINHO_DADOS = Path(__file__).parent.parent.parent / "data" / "pacientes" / "dados.csv"
CABECALHO = ["Data", "Hora", "Batimentos", "Pressão Sistólica", "Pressão Diastólica", "Glicose", "Obs"]

def verificar_arquivo() -> None:
    """Garante que o arquivo existe com cabeçalho correto"""
    if not CAMINHO_DADOS.exists():
        CAMINHO_DADOS.parent.mkdir(parents=True, exist_ok=True)
        with CAMINHO_DADOS.open("w", newline="", encoding="utf-8") as arquivo:
            csv.writer(arquivo).writerow(CABECALHO)

def classificar_exames(batimentos: str, pressao_sist: str, pressao_diast: str, glicose: str) -> str:
    """Classifica os exames usando abordagem funcional"""
    def classificar(valor: str, limites: List[tuple], labels: List[str]) -> str:
        try:
            valor_int = int(valor)
            return next(
                (f"{labels[i]}" for i, (min_v, max_v) in enumerate(limites) if min_v <= valor_int <= max_v),
                "Fora da faixa"
            )
        except ValueError:
            return "Valor inválido"
    
    classificacoes = [
        f"Batimentos: {classificar(batimentos, [(60, 100)], ['Normal'])}",
        f"Pressão: {classificar(pressao_sist, [(0, 119)], ['Normal'])}",
        f"Glicose: {classificar(glicose, [(70, 99)], ['Normal'])}"
    ]
    return "; ".join(classificacoes)

def adicionar_exames() -> None:
    """Função principal para adicionar exames - deve ser importada pelo main.py"""
    verificar_arquivo()
    
    # Coleta de dados
    campos = {
        "Batimentos": "Batimentos cardíacos (bpm): ",
        "Pressão Sistólica": "Pressão sistólica: ",
        "Pressão Diastólica": "Pressão diastólica: ",
        "Glicose": "Nível de glicose (mg/dL): "
    }
    
    valores = {campo: input(mensagem) for campo, mensagem in campos.items()}
    
    # Cria registro
    agora = datetime.now()
    registro = {
        "Data": agora.strftime("%d/%m/%Y"),
        "Hora": agora.strftime("%H:%M:%S"),
        **valores,
        "Obs": classificar_exames(**valores)
    }
    
    # Salva no arquivo
    with CAMINHO_DADOS.open("a", newline="", encoding="utf-8") as arquivo:
        csv.DictWriter(arquivo, fieldnames=CABECALHO).writerow(registro)
    
    print("Exame adicionado com sucesso!")

if __name__ == "__main__":
    adicionar_exames()