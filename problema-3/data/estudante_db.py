"""
Módulo de acesso ao banco de dados para estudantes.

Responsável por criar a tabela, salvar e listar estudantes no banco SQLite.
"""
import json
from data.conexao import conectar

def criar_tabelas():
    """
    Cria as tabelas necessárias no banco de dados, se ainda não existirem.
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

    # Verifica se as novas colunas existem e as adiciona se necessário
    cursor.execute("PRAGMA table_info(estudantes)")
    colunas_existentes = [coluna[1] for coluna in cursor.fetchall()]

    if 'habilidades' not in colunas_existentes:
        cursor.execute("ALTER TABLE estudantes ADD COLUMN habilidades TEXT")
    if 'desempenho_escolar' not in colunas_existentes:
        cursor.execute("ALTER TABLE estudantes ADD COLUMN desempenho_escolar TEXT")

    conn.commit()
    conn.close()


def salvar_estudante(estudante):
    """
    Salva um objeto Estudante no banco de dados.

    Args:
        estudante (Estudante): Objeto contendo os dados do estudante.
    """
    conn = conectar()
    cursor = conn.cursor()
    
    # Converte os dados para JSON
    interesses_json = json.dumps(estudante.interesses)
    habilidades_json = json.dumps(estudante.habilidades)
    desempenho_json = json.dumps(estudante.desempenho_escolar)
    
    # Debug: Imprime os dados antes de salvar
    print("\nDados a serem salvos:")
    print(f"Nome: {estudante.nome}")
    print(f"Interesses: {interesses_json}")
    print(f"Habilidades: {habilidades_json}")
    print(f"Desempenho: {desempenho_json}")
    
    cursor.execute("""
        INSERT INTO estudantes (nome, interesses, habilidades, desempenho_escolar)
        VALUES (?, ?, ?, ?)
    """, (estudante.nome, interesses_json, habilidades_json, desempenho_json))
    
    conn.commit()
    conn.close()


def listar_estudantes():
    """
    Retorna todos os estudantes cadastrados no banco de dados.

    Returns:
    ERRADO!
        list[tuple]: Lista de tuplas contendo (id, nome, interesses, habilidades, desempenho_escolar).
    """
    conn = conectar()
    cursor = conn.cursor()
    
    # Debug: Verifica a estrutura da tabela
    # cursor.execute("PRAGMA table_info(estudantes)")
    # colunas = cursor.fetchall()
    # print("\nEstrutura da tabela:")
    # for coluna in colunas:
    #     print(f"Coluna: {coluna[1]}, Tipo: {coluna[2]}")
    
    # Busca os dados
    cursor.execute("""
        SELECT * FROM estudantes
    """)
    rows = cursor.fetchall()
    
    # # Debug: Imprime os dados brutos
    # print("\nDados brutos do banco:")
    # for row in rows:
    #     print(f"\nID: {row[0]}")
    #     print(f"Nome: {row[1]}")
    #     print(f"Interesses (raw): {row[2]}")
    #     print(f"Habilidades (raw): {row[3]}")
    #     print(f"Desempenho (raw): {row[4]}")
    
    # Converte os dados JSON de volta para objetos Python
    estudantes = []
    for row in rows:
        id_, nome, interesses_json, habilidades_json, desempenho_json = row
        
        # Debug: Imprime os dados após conversão
        print(f"\nProcessando estudante {nome}:")
        
        try:
            interesses = json.loads(interesses_json) if interesses_json else []
            print(f"Interesses convertidos: {interesses}")
        except Exception as e:
            print(f"Erro ao converter interesses: {str(e)}")
            interesses = []
        
        try:
            habilidades = json.loads(habilidades_json) if habilidades_json else []
            print(f"Habilidades convertidas: {habilidades}")
        except Exception as e:
            print(f"Erro ao converter habilidades: {str(e)}")
            habilidades = []
        
        try:
            desempenho = json.loads(desempenho_json) if desempenho_json else {}
            print(f"Desempenho convertido: {desempenho}")
        except Exception as e:
            print(f"Erro ao converter desempenho: {str(e)}")
            desempenho = {}
        
        estudantes.append((id_, nome, interesses, habilidades, desempenho))
    
    conn.close()
    return estudantes

