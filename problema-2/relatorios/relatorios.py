from typing import Dict, List, Callable, Iterator, Tuple, Optional
import csv
from datetime import datetime, timedelta
import os


Registro = Dict[str, str]
Usuario = Dict[str, str]


def obter_caminho_base():
    """Retorna o caminho base do projeto para construir caminhos absolutos"""
    caminho_script = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(caminho_script)


# Filtros adaptados para o formato do CSV
FILTROS_PADRAO = {
    # batimentos cardíacos
    "batimentos_normal": lambda r: 60 <= float(r["Batimentos"]) <= 100,
    "batimentos_alto": lambda r: float(r["Batimentos"]) > 100,
    "batimentos_baixo": lambda r: float(r["Batimentos"]) < 60,
    # pressão arterial
    "pressao_normal": lambda r: 90 <= float(r["Pressão Sistólica"]) <= 120
    and 60 <= float(r["Pressão Diastólica"]) <= 80,
    "pressao_alta": lambda r: float(r["Pressão Sistólica"]) > 140
    or float(r["Pressão Diastólica"]) > 90,
    "pressao_baixa": lambda r: float(r["Pressão Sistólica"]) < 90
    or float(r["Pressão Diastólica"]) < 60,
    # glicose
    "glicose_normal": lambda r: 70 <= float(r["Glicose"]) <= 99,
    "glicose_alta": lambda r: float(r["Glicose"]) > 126,
    "glicose_baixa": lambda r: float(r["Glicose"]) < 70,
}


def classificar_batimentos(valor: float) -> str:
    """Classifica os batimentos cardíacos"""
    if valor < 60:
        return "baixo"
    elif valor > 100:
        return "alto"
    else:
        return "normal"


def classificar_pressao(sistolica: float, diastolica: float) -> str:
    """Classifica a pressão arterial"""
    if sistolica > 140 or diastolica > 90:
        return "alta"
    elif sistolica < 90 or diastolica < 60:
        return "baixa"
    else:
        return "normal"


def classificar_glicose(valor: float) -> str:
    """Classifica o nível de glicose"""
    if valor > 126:
        return "alta"
    elif valor < 70:
        return "baixa"
    else:
        return "normal"


def carregar_dados_pacientes(caminho: str) -> List[Registro]:
    """Carrega dados do arquivo CSV de pacientes"""
    if not os.path.exists(caminho):
        print(f"Arquivo não encontrado: {caminho}")
        return []

    with open(caminho, mode="r", encoding="utf-8") as arquivo:
        registros = list(csv.DictReader(arquivo))
        print(f"Carregados {len(registros)} registros de {caminho}")
        return registros


def filtrar_por_data(
    registros: List[Registro], data_inicio: str, data_fim: str
) -> List[Registro]:
    """
    Filtra registros por período de data no formato brasileiro (dd/mm/aaaa)

    Os registros no CSV já estão no formato brasileiro dd/mm/aaaa,
    então não precisamos converter para comparar.
    """
    print(f"Filtrando registros entre {data_inicio} e {data_fim}")

    # Converte as datas para valores numéricos para comparação correta
    def data_para_numero(data_str):
        if "/" in data_str:
            dia, mes, ano = map(int, data_str.split("/"))
            return ano * 10000 + mes * 100 + dia
        return 0

    data_inicio_num = data_para_numero(data_inicio)
    data_fim_num = data_para_numero(data_fim)

    filtrados = []
    for reg in registros:
        data_reg_num = data_para_numero(reg["Data"])
        if data_inicio_num <= data_reg_num <= data_fim_num:
            filtrados.append(reg)

    return filtrados


def formatar_data_relatorio(data_str: str) -> str:
    """
    Mantém a data no formato brasileiro dd/mm/aaaa
    Os dados já estão neste formato, então apenas retornamos a data
    """
    return data_str


def gerar_relatorio(
    usuario: Dict[str, str],
    tipo_dado: str,
    filtros: Optional[List[Callable]] = None,
    periodo: Optional[Tuple[str, str]] = None,
) -> str:
    """
    Gera um relatório baseado no tipo de dados e filtros

    Args:
        usuario: Informações do usuário
        tipo_dado: 'batimentos', 'pressao' ou 'glicose'
        filtros: Lista de funções de filtro
        periodo: Tupla com (data_inicio, data_fim) no formato dd/mm/aaaa

    Returns:
        Caminho do arquivo de relatório gerado
    """
    caminho_base = obter_caminho_base()
    caminho_dados = os.path.join(caminho_base, "data", "dados_pacientes.csv")

    # Carrega todos os dados
    todos_registros = carregar_dados_pacientes(caminho_dados)
    print(f"Registros antes dos filtros: {len(todos_registros)}")

    # Filtra por data se especificado
    registros = todos_registros
    if periodo:
        registros = filtrar_por_data(registros, *periodo)
        print(f"Registros após filtro de data: {len(registros)}")

    # Aplica filtros adicionais
    if filtros:
        for filtro in filtros:
            registros = [r for r in registros if filtro(r)]
            print(f"Registros após filtro adicional: {len(registros)}")

    # Prepara dados para o relatório
    dados_relatorio = []
    for reg in registros:
        resultado = {
            "Data": formatar_data_relatorio(reg["Data"]),
            "Hora": reg["Hora"],
            "Obs": reg["Obs"],
        }

        if tipo_dado == "batimentos":
            valor = float(reg["Batimentos"])
            resultado["Valor"] = str(valor)
            resultado["Unidade"] = "bpm"
            resultado["Classificação"] = classificar_batimentos(valor)

        elif tipo_dado == "pressao":
            sistolica = float(reg["Pressão Sistólica"])
            diastolica = float(reg["Pressão Diastólica"])
            resultado["Valor"] = f"{sistolica}/{diastolica}"
            resultado["Unidade"] = "mmHg"
            resultado["Classificação"] = classificar_pressao(sistolica, diastolica)

        elif tipo_dado == "glicose":
            valor = float(reg["Glicose"])
            resultado["Valor"] = str(valor)
            resultado["Unidade"] = "mg/dL"
            resultado["Classificação"] = classificar_glicose(valor)

        dados_relatorio.append(resultado)

    # Gera o arquivo CSV
    timestamp = datetime.now().strftime(
        "%d%m%Y_%H%M%S"
    )  # Formato brasileiro para o timestamp
    nome_arquivo = f"{usuario['id']}_{tipo_dado}_{timestamp}.csv"
    caminho_relatorio = os.path.join(caminho_base, "relatorios", nome_arquivo)

    # Garante que o diretório existe
    os.makedirs(os.path.dirname(caminho_relatorio), exist_ok=True)

    # Escreve o relatório
    with open(caminho_relatorio, mode="w", newline="", encoding="utf-8") as arquivo:
        campos = ["Data", "Hora", "Valor", "Classificação", "Unidade", "Obs"]
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(dados_relatorio)

    return caminho_relatorio
