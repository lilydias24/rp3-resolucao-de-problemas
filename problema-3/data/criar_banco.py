"""
Módulo de acesso ao banco de dados para estudantes.

Responsável por criar a tabela, salvar e listar estudantes no banco SQLite.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.conexao import conectar, ConexaoErro

def criar_tabelas():
    """
    Cria todas as tabelas necessárias no banco de dados, incluindo tabelas intermediárias para relacionamentos.
    
    Raises:
        ConexaoErro: Se houver erro ao criar as tabelas
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Tabela de estudantes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estudantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )
        """)
        
        # Tabela de interesses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interesses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interesse TEXT NOT NULL UNIQUE
            )
        """)
        
        # Tabela de habilidades
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habilidades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habilidade TEXT NOT NULL UNIQUE
            )
        """)
        
        # Tabela de disciplinas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS disciplinas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disciplina TEXT NOT NULL UNIQUE
            )
        """)
        
        # Tabela de relacionamento estudantes-interesses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estudantes_interesses (
                estudante_id INTEGER,
                interesse_id INTEGER,
                FOREIGN KEY (estudante_id) REFERENCES estudantes(id) ON DELETE CASCADE,
                FOREIGN KEY (interesse_id) REFERENCES interesses(id) ON DELETE CASCADE,
                PRIMARY KEY (estudante_id, interesse_id)
            )
        """)
        
        # Tabela de relacionamento estudantes-habilidades
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estudantes_habilidades (
                estudante_id INTEGER,
                habilidade_id INTEGER,
                FOREIGN KEY (estudante_id) REFERENCES estudantes(id) ON DELETE CASCADE,
                FOREIGN KEY (habilidade_id) REFERENCES habilidades(id) ON DELETE CASCADE,
                PRIMARY KEY (estudante_id, habilidade_id)
            )
        """)
        
        # Tabela de desempenho
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS desempenho_estudante (
                estudante_id INTEGER,
                disciplina_id INTEGER,
                nota REAL NOT NULL,
                FOREIGN KEY (estudante_id) REFERENCES estudantes(id) ON DELETE CASCADE,
                FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE,
                PRIMARY KEY (estudante_id, disciplina_id)
            )
        """)
        
        # Tabela de regras de carreira
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS regras_carreira (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                carreira TEXT NOT NULL,
                justificativa TEXT
            )
        """)
        
        # Tabelas intermediárias regra de carreira
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS regras_interesses (
                regra_id INTEGER,
                interesse_id INTEGER,
                FOREIGN KEY (regra_id) REFERENCES regras_carreira(id) ON DELETE CASCADE,
                FOREIGN KEY (interesse_id) REFERENCES interesses(id) ON DELETE CASCADE,
                PRIMARY KEY (regra_id, interesse_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS regras_habilidades (
                regra_id INTEGER,
                habilidade_id INTEGER,
                FOREIGN KEY (regra_id) REFERENCES regras_carreira(id) ON DELETE CASCADE,
                FOREIGN KEY (habilidade_id) REFERENCES habilidades(id) ON DELETE CASCADE,
                PRIMARY KEY (regra_id, habilidade_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS regras_desempenho (
                regra_id INTEGER,
                disciplina_id INTEGER,
                nota_min REAL NOT NULL,
                peso REAL DEFAULT 1,
                FOREIGN KEY (regra_id) REFERENCES regras_carreira(id) ON DELETE CASCADE,
                FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE,
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
                FOREIGN KEY (estudante_id) REFERENCES estudantes(id) ON DELETE CASCADE
            )
        """)
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        raise ConexaoErro(f"Erro ao criar tabelas: {str(e)}")

if __name__ == "__main__":
    criar_tabelas()




