"""
Módulo de acesso ao banco de dados para estudantes.

Responsável por criar a tabela, salvar e listar estudantes no banco SQLite.
"""
import json
from data.conexao import conectar

def criar_tabela_estudantes():
    """
    Cria a tabela 'estudantes' no banco de dados, se ainda não existir.

    A tabela contém:
    - id (int): identificador único do estudante.
    - interesses (text): interesses em formato JSON.
    """
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS estudantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            interesses TEXT
        )
    """)
    con.commit()
    con.close()


def salvar_estudante(estudante):
    """
    Salva um objeto Estudante no banco de dados.

    Args:
        estudante (Estudante): Objeto contendo os dados do estudante.
    """
    con = conectar()
    cur = con.cursor()
    interesses_json = json.dumps(estudante.interesses)
    cur.execute("INSERT INTO estudantes (nome, interesses) VALUES (?, ?)", (estudante.nome, interesses_json))
    con.commit()
    con.close()


def listar_estudantes():
    """
    Retorna todos os estudantes cadastrados no banco de dados.

    Returns:
        list[tuple]: Lista de tuplas (id, nome, interesses_json).
    """
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, nome, interesses FROM estudantes")
    rows = cur.fetchall()
    con.close()
    return rows

