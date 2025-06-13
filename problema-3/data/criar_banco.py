"""
Módulo de acesso ao banco de dados para estudantes.

Responsável por criar a tabela, salvar e listar estudantes no banco SQLite.
"""

from data.conexao import conectar

def criar_tabelas():
    """
    Cria todas as tabelas necessárias no banco de dados, incluindo tabelas intermediárias para relacionamentos.
    """
    conn = conectar()
    cursor = conn.cursor()

    # Tabela de estudantes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estudantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)

    # Tabelas de domínio
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disciplinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disciplina TEXT NOT NULL UNIQUE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habilidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habilidade TEXT NOT NULL UNIQUE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interesse TEXT NOT NULL UNIQUE
        )
    """)

    # Tabelas intermediárias estudante
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habilidades_estudante (
            estudante_id INTEGER,
            habilidade_id INTEGER,
            FOREIGN KEY (estudante_id) REFERENCES estudantes(id),
            FOREIGN KEY (habilidade_id) REFERENCES habilidades(id),
            PRIMARY KEY (estudante_id, habilidade_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interesses_estudante (
            estudante_id INTEGER,
            interesse_id INTEGER,
            FOREIGN KEY (estudante_id) REFERENCES estudantes(id),
            FOREIGN KEY (interesse_id) REFERENCES interesses(id),
            PRIMARY KEY (estudante_id, interesse_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS desempenho_estudante (
            estudante_id INTEGER,
            disciplina_id INTEGER,
            nota REAL NOT NULL,
            FOREIGN KEY (estudante_id) REFERENCES estudantes(id),
            FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id),
            PRIMARY KEY (estudante_id, disciplina_id)
        )
    """)

    # Tabela de regras de carreira (antes era o JSON)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS regras_carreira (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            carreira TEXT NOT NULL,
            justificativa TEXT
        )
    """)
    # Tabelas intermediárias regra de carreira
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interesses_regra (
            regra_id INTEGER,
            interesse_id INTEGER,
            FOREIGN KEY (regra_id) REFERENCES regras_carreira(id),
            FOREIGN KEY (interesse_id) REFERENCES interesses(id),
            PRIMARY KEY (regra_id, interesse_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habilidades_regra (
            regra_id INTEGER,
            habilidade_id INTEGER,
            FOREIGN KEY (regra_id) REFERENCES regras_carreira(id),
            FOREIGN KEY (habilidade_id) REFERENCES habilidades(id),
            PRIMARY KEY (regra_id, habilidade_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS desempenho_regra (
            regra_id INTEGER,
            disciplina_id INTEGER,
            nota_min REAL NOT NULL,
            peso REAL DEFAULT 1,
            FOREIGN KEY (regra_id) REFERENCES regras_carreira(id),
            FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id),
            PRIMARY KEY (regra_id, disciplina_id)
        )
    """)

    # Tabela de recomendações
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recomendacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudante_id INTEGER NOT NULL,
            carreira TEXT NOT NULL,
            score REAL,
            data_recomendacao TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (estudante_id) REFERENCES estudantes(id)
        )
    """)

    conn.commit()
    conn.close()




