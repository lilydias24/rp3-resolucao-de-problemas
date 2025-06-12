import sqlite3
from data.conexao import conectar

def salvar_recomendacao(estudante_id, carreira, score):
    """
    Salva uma recomendação de carreira para um estudante no banco de dados.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO recomendacoes (estudante_id, carreira, score) VALUES (?, ?, ?)",
        (estudante_id, carreira, score)
    )
    conn.commit()
    conn.close()

def listar_recomendacoes():
    """
    Lista todas as recomendações feitas para todos os estudantes.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT estudante_id, carreira, score, data_recomendacao FROM recomendacoes
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows