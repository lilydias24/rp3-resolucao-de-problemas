"""
Módulo de acesso ao banco de dados para estudantes.

Responsável por criar a tabela, salvar e listar estudantes no banco SQLite.
"""
import json
from data.conexao import conectar

def criar_tabela_estudantes():
    """
    Cria a tabela 'estudantes' no banco de dados, se ainda não existir.
    Se a tabela já existir, adiciona as novas colunas necessárias.

    A tabela contém:
    - id (int): identificador único do estudante
    - nome (text): nome do estudante
    - interesses (text): interesses em formato JSON
    - habilidades (text): habilidades em formato JSON
    - desempenho_escolar (text): desempenho acadêmico em formato JSON
    """
    con = conectar()
    cur = con.cursor()
    
    # cria se n existir
    cur.execute("""
        CREATE TABLE IF NOT EXISTS estudantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            interesses TEXT,
            habilidades TEXT,
            desempenho_escolar TEXT
        )
    """)
    
    # verifica se as novas colunas existem e as adiciona se necessário
    cur.execute("PRAGMA table_info(estudantes)")
    colunas_existentes = [coluna[1] for coluna in cur.fetchall()]
    
    if 'habilidades' not in colunas_existentes:
        cur.execute("ALTER TABLE estudantes ADD COLUMN habilidades TEXT")
    
    if 'desempenho_escolar' not in colunas_existentes:
        cur.execute("ALTER TABLE estudantes ADD COLUMN desempenho_escolar TEXT")
    
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
    
    # joga os dados pra json
    interesses_json = json.dumps(estudante.interesses)
    habilidades_json = json.dumps(estudante.habilidades)
    desempenho_json = json.dumps(estudante.desempenho_escolar)
    
    # debug: imprime os dados antes de salvar
    print("\nDados a serem salvos:")
    print(f"Nome: {estudante.nome}")
    print(f"Interesses: {interesses_json}")
    print(f"Habilidades: {habilidades_json}")
    print(f"Desempenho (raw): {desempenho_json}")
    print(f"Desempenho (dict): {estudante.desempenho_escolar}")
    
    cur.execute("""
        INSERT INTO estudantes (nome, interesses, habilidades, desempenho_escolar)
        VALUES (?, ?, ?, ?)
    """, (estudante.nome, interesses_json, habilidades_json, desempenho_json))
    
    con.commit()
    con.close()


def listar_estudantes():
    """
    Retorna todos os estudantes cadastrados no banco de dados.

    Returns:
        list[tuple]: Lista de tuplas contendo (id, nome, interesses, habilidades, desempenho_escolar).
    """
    con = conectar()
    cur = con.cursor()
    
    # debug: verifica a estrutura da tabela
    cur.execute("PRAGMA table_info(estudantes)")
    colunas = cur.fetchall()
    print("\nEstrutura da tabela:")
    for coluna in colunas:
        print(f"Coluna: {coluna[1]}, Tipo: {coluna[2]}")
    
    cur.execute("""
        SELECT id, nome, interesses, habilidades, desempenho_escolar 
        FROM estudantes
    """)
    rows = cur.fetchall()
    
    # debug: imprime os dados brutos
    print("\nDados brutos do banco:")
    for row in rows:
        print(f"\nID: {row[0]}")
        print(f"Nome: {row[1]}")
        print(f"Interesses (raw): {row[2]}")
        print(f"Habilidades (raw): {row[3]}")
        print(f"Desempenho (raw): {row[4]}")
    
    # converte os dados json de volta para objetos python
    estudantes = []
    for row in rows:
        id_, nome, interesses_json, habilidades_json, desempenho_json = row
        
        # debug: imprime os dados dps conversão
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
            print(f"Desempenho (tipo): {type(desempenho)}")
            print(f"Desempenho (chaves): {list(desempenho.keys())}")
            print(f"Desempenho (valores): {list(desempenho.values())}")
        except Exception as e:
            print(f"Erro ao converter desempenho: {str(e)}")
            desempenho = {}
        
        estudantes.append((id_, nome, interesses, habilidades, desempenho))
    
    con.close()
    return estudantes

