from typing import Dict, List, Optional
import csv
from datetime import datetime
import os

def obter_caminho_base():
    """Retorna o caminho base do projeto"""
    caminho_script = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(caminho_script)

def carregar_dados(caminho: str) -> List[Dict]:
    """Carrega dados do arquivo CSV"""
    if not os.path.exists(caminho):
        print(f"Arquivo não encontrado: {caminho}")
        return []
    
    try:
        with open(caminho, mode='r', encoding='utf-8') as arquivo:
            registros = list(csv.DictReader(arquivo))
            print(f"Carregados {len(registros)} registros")
            return registros
    except Exception as e:
        print(f"Erro ao carregar dados: {str(e)}")
        return []

def gerar_relatorio(dados: List[Dict], formato: str) -> str:
    """
    Gera um relatório com os dados fornecidos
    
    Args:
        dados: Lista de dicionários com os dados
        formato: 'csv' ou 'json'
    
    Returns:
        Caminho do arquivo de relatório gerado
    """
    if not dados:
        raise ValueError("Nenhum dado fornecido para o relatório")
    
    # Cria diretório para relatórios se não existir
    caminho_base = obter_caminho_base()
    dir_relatorios = os.path.join(caminho_base, "relatorios")
    os.makedirs(dir_relatorios, exist_ok=True)
    
    # Gera nome do arquivo com timestamp
    timestamp = datetime.now().strftime('%d%m%Y_%H%M%S')
    nome_arquivo = f"relatorio_{timestamp}.{formato}"
    caminho_relatorio = os.path.join(dir_relatorios, nome_arquivo)
    
    try:
        if formato == 'csv':
            # Escreve relatório CSV
            with open(caminho_relatorio, mode='w', newline='', encoding='utf-8') as arquivo:
                if dados:
                    campos = dados[0].keys()
                    escritor = csv.DictWriter(arquivo, fieldnames=campos)
                    escritor.writeheader()
                    escritor.writerows(dados)
        
        elif formato == 'json':
            # Escreve relatório JSON
            import json
            with open(caminho_relatorio, mode='w', encoding='utf-8') as arquivo:
                json.dump(dados, arquivo, indent=2, ensure_ascii=False)
        
        print(f"Relatório gerado com sucesso: {caminho_relatorio}")
        return caminho_relatorio
        
    except Exception as e:
        print(f"Erro ao gerar relatório: {str(e)}")
        raise

if __name__ == "__main__":
    # Teste do módulo
    caminho_dados = os.path.join(obter_caminho_base(), "dados", "dados_pacientes.csv")
    dados = carregar_dados(caminho_dados)
    if dados:
        gerar_relatorio(dados, "csv") 