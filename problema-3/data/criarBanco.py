"""
Módulo de acesso ao banco de dados para estudantes.

Responsável por criar a tabela, salvar e listar estudantes no banco SQLite.
"""

from data.conexao import conectar

def criar_tabelas():
    """
    Cria as tabelas necessárias no banco de dados, se ainda não existirem. Cria tabelas primárias para estudantes, disciplinas, 
    habilidades, interesses e desempenho, e define as relações entre elas.
    Esta função deve ser chamada uma vez para garantir que o esquema do banco de dados esteja configurado corretamente.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estudantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disciplinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disciplina TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habilidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habilidade TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interesse TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS desempenho_estudante (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudante_id INTEGER NOT NULL,
            disciplina_id TEXT NOT NULL,
            nota REAL NOT NULL,
            FOREIGN KEY (estudante_id) REFERENCES estudantes(id),
            FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habilidades_estudante (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudante_id INTEGER NOT NULL,
            habilidade_id TEXT NOT NULL,
            FOREIGN KEY (estudante_id) REFERENCES estudantes(id),
            FOREIGN KEY (habilidade_id) REFERENCES habilidades(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interesses_estudante (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudante_id INTEGER NOT NULL,
            interesse_id TEXT NOT NULL,
            FOREIGN KEY (estudante_id) REFERENCES estudantes(id),
            FOREIGN KEY (interesse_id) REFERENCES interesses(id)
        )
    """)

    conn.commit()
    conn.close()




