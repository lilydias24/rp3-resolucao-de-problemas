"""Gerador conjuntos de dados médicos sintéticos (batimentos cardíacos, pressão arterial, glicose) no formato CSV.

Como usar:

python3 -B gerador_dataset_saude.py --linhas 10000 --caracteres 900000 --nome-arquivo dataset_saude.csv
"""

# Importando dependências
import csv
import random
from datetime import datetime, timedelta
import os

def gerar_dataset_csv(num_registros: int) -> str:
    """
    Gera um dataset sintético de dados médicos em formato CSV.
    
    Args:
        num_registros: Número de registros a serem gerados
        
    Returns:
        str: Caminho do arquivo CSV gerado
    """
    # Cria diretório para datasets se não existir
    caminho_base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dir_datasets = os.path.join(caminho_base, "dados")
    os.makedirs(dir_datasets, exist_ok=True)
    
    # Nome do arquivo com timestamp
    timestamp = datetime.now().strftime('%d%m%Y_%H%M%S')
    nome_arquivo = f"dataset_saude_{timestamp}.csv"
    caminho_arquivo = os.path.join(dir_datasets, nome_arquivo)
    
    # Gera dados sintéticos
    with open(caminho_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
        campos = ['Data', 'Hora', 'Batimentos', 'Pressão', 'Glicose', 'Obs']
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        
        # Data inicial (30 dias atrás)
        data_inicial = datetime.now() - timedelta(days=30)
        
        for _ in range(num_registros):
            # Gera data e hora
            data = data_inicial + timedelta(days=random.randint(0, 30))
            hora = datetime.strptime(f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}", "%H:%M:%S")
            
            # Gera valores médicos
            batimentos = random.randint(60, 100)
            pressao_sistolica = random.randint(110, 140)
            pressao_diastolica = random.randint(70, 90)
            glicose = random.randint(70, 140)
            
            # Gera observações
            obs = []
            if batimentos > 90:
                obs.append("Batimentos: Taquicardia")
            elif batimentos < 70:
                obs.append("Batimentos: Bradicardia")
                
            if pressao_sistolica > 130 or pressao_diastolica > 85:
                obs.append("Pressão: Pré-hipertensão")
            elif pressao_sistolica < 110 or pressao_diastolica < 70:
                obs.append("Pressão: Hipotensão")
                
            if glicose > 126:
                obs.append("Glicose: Hiperglicemia")
            elif glicose < 70:
                obs.append("Glicose: Hipoglicemia")
            
            # Escreve registro
            escritor.writerow({
                'Data': data.strftime('%d/%m/%Y'),
                'Hora': hora.strftime('%H:%M:%S'),
                'Batimentos': str(batimentos),
                'Pressão': f"{pressao_sistolica}/{pressao_diastolica}",
                'Glicose': str(glicose),
                'Obs': '; '.join(obs) if obs else ''
            })
    
    return caminho_arquivo

if __name__ == "__main__":
    # Teste do módulo
    gerar_dataset_csv(10)
