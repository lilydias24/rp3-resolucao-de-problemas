from typing import Dict, List, Callable, Iterator, Tuple, Optional
import csv
from datetime import datetime, timedelta
from functools import partial
import os


Registro = Dict[str, str]
Usuario = Dict[str, str]

#  func pra obter o caminho base do projeto
def obter_caminho_base():
    """Retorna o caminho base do projeto para construir caminhos absolutos"""
    # da o diretorio do script atual
    caminho_script = os.path.dirname(os.path.abspath(__file__))
    return caminho_script

# filtros puros
FILTROS_PADRAO = {
    # batimentos cardíacos
    'batimentos_normal': lambda r: 60 <= float(r['valor']) <= 100,
    'batimentos_alto': lambda r: float(r['valor']) > 100,
    'batimentos_baixo': lambda r: float(r['valor']) < 60,
    'batimentos_critico': lambda r: float(r['valor']) < 50 or float(r['valor']) > 120,
    
    # preessão arterial
    'pressao_normal': lambda r: 90 <= float(r['valor'].split('/')[0]) <= 120 and 60 <= float(r['valor'].split('/')[1]) <= 80,
    'pressao_alta': lambda r: float(r['valor'].split('/')[0]) > 140 or float(r['valor'].split('/')[1]) > 90,
    
    # glicose
    'glicose_normal': lambda r: 70 <= float(r['valor']) <= 99,
    'glicose_alta': lambda r: float(r['valor']) > 126,
    'glicose_baixa': lambda r: float(r['valor']) < 70
}

# func de transf puras
def classificar_registro(registro: Registro, tipo_dado: str) -> Registro:
    """Adiciona classificação aos registros baseado no tipo de dado"""
    valor = registro['valor']
    
    if tipo_dado == 'batimentos':
        valor_float = float(valor)
        classificacao = (
            "critico" if valor_float < 50 or valor_float > 120 else
            "alto" if valor_float > 100 else
            "baixo" if valor_float < 60 else
            "normal"
        )
    elif tipo_dado == 'pressao':
        sistolica, diastolica = map(float, valor.split('/'))
        classificacao = (
            "alta" if sistolica > 140 or diastolica > 90 else
            "normal" if 90 <= sistolica <= 120 and 60 <= diastolica <= 80 else
            "baixa"
        )
    elif tipo_dado == 'glicose':
        valor_float = float(valor)
        classificacao = (
            "alta" if valor_float > 126 else
            "baixa" if valor_float < 70 else
            "normal"
        )
    else:
        classificacao = "indefinido"
    
    return {**registro, 'classificacao': classificacao}

def converter_formato_data(data_str: str) -> str:
    """Converte data do formato dd-mm-yyyy para yyyy-mm-dd para comparação"""
    if '-' in data_str and len(data_str.split('-')) == 3:
       
        dia, mes, ano = data_str.split('-')
        if len(dia) == 2 and len(mes) == 2 and len(ano) == 4:
            return f"{ano}-{mes}-{dia}"
    return data_str 

def converter_formato_data_para_exibicao(data_str: str) -> str:
    """Converte data do formato yyyy-mm-dd para dd-mm-yyyy para exibição"""
    if '-' in data_str and len(data_str.split('-')) == 3:
        
        ano, mes, dia = data_str.split('-')
        if len(ano) == 4 and len(mes) == 2 and len(dia) == 2:
            return f"{dia}-{mes}-{ano}"
    return data_str  

# func de filtro pura
def filtrar_por_data(registros: Iterator[Registro], data_inicio: str, data_fim: str) -> Iterator[Registro]:
    """Filtra registros por período"""
    
    data_inicio_iso = converter_formato_data(data_inicio)
    data_fim_iso = converter_formato_data(data_fim)
    
    return filter(
        lambda r: data_inicio_iso <= r['data'] <= data_fim_iso,
        registros
    )

def filtrar_por_valor(registros: Iterator[Registro], filtro: Callable) -> Iterator[Registro]:
    """Aplica um filtro de valor aos registros"""
    return filter(filtro, registros)

# func de carregamento 
def carregar_dados_saude(caminho: str) -> List[Registro]:
    """Carrega dados de saúde de um arquivo CSV"""
    if not os.path.exists(caminho):
        print(f"Arquivo não encontrado: {caminho}")
        return []
    
    with open(caminho, mode='r', encoding='utf-8') as arquivo:
        registros = list(csv.DictReader(arquivo))
        print(f"Carregados {len(registros)} registros de {caminho}")
        return registros

# func de gerar relatorio
def gerar_relatorio_csv(usuario: Usuario, registros: List[Registro], caminho: str) -> None:
    """Gera relatório em formato CSV"""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    
    # Converte as datas para o formato dd-mm-yyyy antes de escrever no relatório
    registros_formatados = []
    for registro in registros:
        registro_formatado = registro.copy()
        registro_formatado['data'] = converter_formato_data_para_exibicao(registro['data'])
        registros_formatados.append(registro_formatado)
    
    with open(caminho, mode='w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=['data', 'valor', 'classificacao', 'unidade'])
        escritor.writeheader()
        escritor.writerows(registros_formatados)

# func principal de gerar relatorio
def gerar_relatorio(
    usuario: Usuario,
    tipo_dado: str,
    filtros: Optional[List[Callable]] = None,
    periodo: Optional[Tuple[str, str]] = None
) -> str:
    """
    Gera um relatório de saúde para o usuário em formato CSV.
    
    Args:
        usuario: dicionario com informações do usuário
        tipo_dado: tipo de dado a ser analisado ('batimentos', 'pressao', 'glicose')
        filtros: lista de funções de filtro a serem aplicadas
        periodo: tupla com data de início e fim no formato 'dd-mm-yyyy'
    
    Returns:
        Caminho do arquivo gerado
    """
    # da o caminho base do projeto
    caminho_base = obter_caminho_base()
    
    # carrega dados
    caminho_dados = os.path.join(caminho_base, "dados", f"paciente_{usuario['id']}", f"{tipo_dado}.csv")
    registros = carregar_dados_saude(caminho_dados)
    
    print(f"Registros antes dos filtros: {len(registros)}")
    
    # aplica filtros
    if periodo:
        registros = list(filtrar_por_data(registros, *periodo))
        print(f"Registros após filtro de data: {len(registros)}")
    
    if filtros:
        for filtro in filtros:
            registros = list(filtrar_por_valor(registros, filtro))
            print(f"Registros após filtro de valor: {len(registros)}")
    
    # classifica registros
    registros = [classificar_registro(r, tipo_dado) for r in registros]
    
    # gera arquivo
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    caminho_relatorio = os.path.join(caminho_base, "relatorios", f"{usuario['id']}_{tipo_dado}_{timestamp}.csv")
    
    # garante que o diretorio relatorios existe
    os.makedirs(os.path.dirname(caminho_relatorio), exist_ok=True)
    
    gerar_relatorio_csv(usuario, registros, caminho_relatorio)
    
    return caminho_relatorio 