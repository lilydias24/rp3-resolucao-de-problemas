import sys
import os
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def exportar_tendencias_para_csv(caminho_csv):
    """
    Exporta um relatório agregado de tendências de carreira (quantidade de recomendações por carreira) para CSV.
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
# Exemplo de uso:
exportar_tendencias_para_csv('reports/tendencias_carreira.csv')