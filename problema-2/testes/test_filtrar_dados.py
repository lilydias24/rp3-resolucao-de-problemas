import pytest
from src.analise.filtrar_dados import (
    carregar_dados,
    filtrar_registros,
    obter_criterios_padrao,
)
from pathlib import Path
import csv
import os

# Caminho para o arquivo original
CAMINHO_ARQUIVO = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "dados", "pacientes", "dados.csv")
)

# Dados de exemplo para teste
DADOS_EXEMPLO = [
    {
        "Batimentos": "75",
        "Pressão Sistólica": "110",
        "Pressão Diastólica": "70",
        "Glicose": "85",
    },
    {
        "Batimentos": "55",
        "Pressão Sistólica": "130",
        "Pressão Diastólica": "90",
        "Glicose": "120",
    },
    {
        "Batimentos": "101",
        "Pressão Sistólica": "119",
        "Pressão Diastólica": "79",
        "Glicose": "99",
    },
    {
        "Batimentos": "80",
        "Pressão Sistólica": "121",
        "Pressão Diastólica": "70",
        "Glicose": "60",
    },
    {
        "Batimentos": "90",
        "Pressão Sistólica": "115",
        "Pressão Diastólica": "75",
        "Glicose": "100",
    },
]


def salvar_dados_exemplo():
    os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
    with open(CAMINHO_ARQUIVO, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=DADOS_EXEMPLO[0].keys())
        writer.writeheader()
        writer.writerows(DADOS_EXEMPLO)


def test_carregar_dados():
    salvar_dados_exemplo()
    registros = carregar_dados(Path(CAMINHO_ARQUIVO))
    assert isinstance(registros, list)
    assert len(registros) == len(DADOS_EXEMPLO)
    assert registros[0]["Batimentos"] == "75"


def test_filtrar_registros_funcional():
    salvar_dados_exemplo()
    registros = carregar_dados(Path(CAMINHO_ARQUIVO))
    criterios = obter_criterios_padrao()
    resultados = filtrar_registros(registros, criterios)
    # Batimentos fora do padrão: 55, 101
    assert any(r["Batimentos"] == "55" for r in resultados["Batimentos"])
    assert any(r["Batimentos"] == "101" for r in resultados["Batimentos"])
    # Pressão Sistólica fora do padrão: 130, 121
    assert any(r["Pressão Sistólica"] == "130" for r in resultados["Pressão Sistólica"])
    assert any(r["Pressão Sistólica"] == "121" for r in resultados["Pressão Sistólica"])
    # Pressão Diastólica fora do padrão: 90
    assert any(
        r["Pressão Diastólica"] == "90" for r in resultados["Pressão Diastólica"]
    )
    # Glicose fora do padrão: 120, 60, 100
    assert any(r["Glicose"] == "120" for r in resultados["Glicose"])
    assert any(r["Glicose"] == "60" for r in resultados["Glicose"])
    assert any(r["Glicose"] == "100" for r in resultados["Glicose"])


def test_obter_criterios_padrao():
    criterios = obter_criterios_padrao()
    assert callable(criterios["Batimentos"])
    assert criterios["Batimentos"]("75") is True
    assert criterios["Batimentos"]("55") is False
    assert criterios["Pressão Sistólica"]("110") is True
    assert criterios["Pressão Sistólica"]("130") is False
    assert criterios["Glicose"]("85") is True
    assert criterios["Glicose"]("120") is False
