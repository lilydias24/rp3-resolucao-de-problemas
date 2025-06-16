import sys
import os
import csv
from typing import List, Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def exportar_estudantes_para_csv(caminho_csv: str) -> None:
    """
    Exporta a lista de estudantes para CSV.
    
    Args:
        caminho_csv: Caminho do arquivo CSV de saída
    """
    from data.conexao import conectar
    from logic.estudante import listar_estudantes
    
    estudantes = listar_estudantes()
    
    with open(caminho_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Nome', 'Interesses', 'Habilidades', 'Desempenho'])
        for id, nome, interesses, habilidades, desempenho in estudantes:
            writer.writerow([
                id,
                nome,
                ', '.join(interesses) if interesses else '',
                ', '.join(habilidades) if habilidades else '',
                ', '.join(f"{disc}: {nota}" for disc, nota in desempenho.items()) if desempenho else ''
            ])
    
    print(f"Lista de estudantes exportada para {caminho_csv} com sucesso!")

def exportar_regras_para_csv(caminho_csv: str) -> None:
    """
    Exporta a lista de regras de carreira para CSV.
    
    Args:
        caminho_csv: Caminho do arquivo CSV de saída
    """
    from logic.recomendacao import listar_regras
    
    regras = listar_regras()
    
    with open(caminho_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Carreira', 'Condições', 'Peso'])
        for regra in regras:
            writer.writerow([
                regra['id'],
                regra['carreira'],
                ', '.join(regra['condicoes']),
                regra['peso']
            ])
    
    print(f"Lista de regras exportada para {caminho_csv} com sucesso!")

def exportar_estatisticas_para_csv(caminho_csv: str) -> None:
    """
    Exporta estatísticas do sistema para CSV.
    
    Args:
        caminho_csv: Caminho do arquivo CSV de saída
    """
    from data.conexao import conectar
    from logic.estudante import listar_estudantes
    from logic.recomendacao import listar_regras
    from datetime import datetime
    
    estudantes = listar_estudantes()
    regras = listar_regras()
    
    stats = {
        'total_estudantes': len(estudantes),
        'total_regras': len(regras),
        'data_geracao': datetime.now().isoformat()
    }
    
    with open(caminho_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Métrica', 'Valor'])
        for key, value in stats.items():
            writer.writerow([key, value])
    
    print(f"Estatísticas exportadas para {caminho_csv} com sucesso!")

def exportar_tendencias_para_csv(caminho_csv: str) -> None:
    """
    Exporta um relatório agregado de tendências de carreira (quantidade de recomendações por carreira) para CSV.
    
    Args:
        caminho_csv: Caminho do arquivo CSV de saída
    """
    from data.conexao import conectar
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT carreira, COUNT(*) as total
        FROM recomendacoes
        GROUP BY carreira
        ORDER BY total DESC
    """)
    resultados = cursor.fetchall()
    conn.close()

    with open(caminho_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Carreira', 'Total de Recomendações'])
        for carreira, total in resultados:
            writer.writerow([carreira, total])
    
    print(f"Tendências de carreira exportadas para {caminho_csv} com sucesso!")

def exportar_todos_relatorios_csv() -> None:
    """
    Exporta todos os relatórios para CSV.
    """
    # Cria diretório para relatórios CSV
    relatorios_dir = 'reports/relatorios_csv'
    os.makedirs(relatorios_dir, exist_ok=True)
    
    # Exporta cada tipo de relatório
    exportar_estudantes_para_csv(os.path.join(relatorios_dir, 'estudantes.csv'))
    exportar_regras_para_csv(os.path.join(relatorios_dir, 'regras.csv'))
    exportar_estatisticas_para_csv(os.path.join(relatorios_dir, 'estatisticas.csv'))
    exportar_tendencias_para_csv(os.path.join(relatorios_dir, 'tendencias.csv'))
    
    print("Todos os relatórios foram exportados para CSV com sucesso!")

if __name__ == "__main__":
    exportar_todos_relatorios_csv()