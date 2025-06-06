import sys
import os
import csv
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.estudante_db import listar_estudantes

def exportar_estudantes_para_csv(caminho_csv):
    """
    Exporta todos os estudantes do banco SQLite para um arquivo CSV,
    incluindo nome, interesses, habilidades e desempenho escolar.
    """
    estudantes = listar_estudantes()
    if not estudantes:
        print("Nenhum estudante encontrado.")
        return

    # Cabeçalho do CSV
    campos = ['id', 'nome', 'interesses', 'habilidades', 'desempenho_escolar']

    with open(caminho_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(campos)
        for est in estudantes:
            # est[2], est[3], est[4] podem ser JSON ou listas/dicts
            interesses = json.dumps(est[2]) if not isinstance(est[2], str) else est[2]
            habilidades = json.dumps(est[3]) if not isinstance(est[3], str) else est[3]
            desempenho = json.dumps(est[4]) if not isinstance(est[4], str) else est[4]
            writer.writerow([est[0], est[1], interesses, habilidades, desempenho])

# Exemplo de uso:
exportar_estudantes_para_csv('reports/estudantes.csv')