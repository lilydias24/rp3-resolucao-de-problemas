import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from data.conexao import conectar

def importar_regras_json_para_banco(caminho_json):
    """
    Importa regras de carreira de um arquivo JSON e insere no banco de dados,
    preenchendo as tabelas regras_carreira, interesses, habilidades, disciplinas e tabelas intermediárias.
    """
    with open(caminho_json, encoding='utf-8') as f:
        regras = json.load(f)

    conn = conectar()
    cursor = conn.cursor()

    for regra in regras:
        carreira = regra['carreira']
        justificativa = regra.get('justificativa', '')
        condicoes = regra['condicoes']
        interesses = condicoes.get('interesses', [])
        habilidades = condicoes.get('habilidades', [])
        desempenho = condicoes.get('desempenho', {})
        pesos = condicoes.get('pesos', {})

        # Insere regra de carreira
        cursor.execute(
            "INSERT INTO regras_carreira (carreira, justificativa) VALUES (?, ?)",
            (carreira, justificativa)
        )
        regra_id = cursor.lastrowid

        # Interesses
        for interesse in interesses:
            cursor.execute("INSERT OR IGNORE INTO interesses (interesse) VALUES (?)", (interesse,))
            cursor.execute("SELECT id FROM interesses WHERE interesse = ?", (interesse,))
            interesse_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO regras_interesses (regra_id, interesse_id) VALUES (?, ?)", (regra_id, interesse_id))

        # Habilidades
        for habilidade in habilidades:
            cursor.execute("INSERT OR IGNORE INTO habilidades (habilidade) VALUES (?)", (habilidade,))
            cursor.execute("SELECT id FROM habilidades WHERE habilidade = ?", (habilidade,))
            habilidade_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO regras_habilidades (regra_id, habilidade_id) VALUES (?, ?)", (regra_id, habilidade_id))

        # Desempenho (disciplinas, nota mínima e peso)
        for disciplina, nota_min in desempenho.items():
            cursor.execute("INSERT OR IGNORE INTO disciplinas (disciplina) VALUES (?)", (disciplina,))
            cursor.execute("SELECT id FROM disciplinas WHERE disciplina = ?", (disciplina,))
            disciplina_id = cursor.fetchone()[0]
            peso = pesos.get(disciplina, 1)
            cursor.execute(
                "INSERT INTO regras_desempenho (regra_id, disciplina_id, nota_min, peso) VALUES (?, ?, ?, ?)",
                (regra_id, disciplina_id, nota_min, peso)
            )

    conn.commit()
    conn.close()

# Exemplo de uso:
caminho_json = os.path.join(os.path.dirname(__file__), 'regras.json')
importar_regras_json_para_banco(caminho_json)