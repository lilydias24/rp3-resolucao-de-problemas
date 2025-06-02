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
    
    # Cria a tabela se não existir
    cur.execute("""
        CREATE TABLE IF NOT EXISTS estudantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            interesses TEXT,
            habilidades TEXT,
            desempenho_escolar TEXT
        )
    """)
    
    # Verifica se as novas colunas existem e as adiciona se necessário
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
    
    # Converte o estudante para dicionário
    dados = estudante.to_dict()
    
    # Garante que o desempenho seja um dicionário
    if not isinstance(dados['desempenho'], dict):
        dados['desempenho'] = {}
    
    # Converte os dados para JSON
    interesses_json = json.dumps(dados['interesses'])
    habilidades_json = json.dumps(dados['habilidades'])
    desempenho_json = json.dumps(dados['desempenho'])
    
    cur.execute("""
        INSERT INTO estudantes (nome, interesses, habilidades, desempenho_escolar)
        VALUES (?, ?, ?, ?)
    """, (dados['nome'], interesses_json, habilidades_json, desempenho_json))
    
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
    
    # Busca os dados
    cur.execute("""
        SELECT id, nome, interesses, habilidades, desempenho_escolar 
        FROM estudantes
    """)
    rows = cur.fetchall()
    
    # Converte os dados JSON de volta para objetos Python
    estudantes = []
    for row in rows:
        id_, nome, interesses_json, habilidades_json, desempenho_json = row
        
        try:
            interesses = json.loads(interesses_json) if interesses_json else []
        except Exception:
            interesses = []
        
        try:
            habilidades = json.loads(habilidades_json) if habilidades_json else []
        except Exception:
            habilidades = []
        
        try:
            desempenho = json.loads(desempenho_json) if desempenho_json else {}
        except Exception:
            desempenho = {}
        
        estudantes.append((id_, nome, interesses, habilidades, desempenho))
    
    con.close()
    return estudantes

def obter_disciplinas():
    """
    Retorna a lista de todas as disciplinas registradas no banco.
    
    Returns:
        list: Lista de nomes de disciplinas
    """
    con = conectar()
    cur = con.cursor()
    
    cur.execute("SELECT DISTINCT json_extract(desempenho_escolar, '$.*') FROM estudantes")
    disciplinas = set()
    for row in cur.fetchall():
        if row[0]:
            desempenho = json.loads(row[0])
            disciplinas.update(desempenho.keys())
    
    con.close()
    return sorted(list(disciplinas))

def obter_desempenho_disciplina(disciplina: str):
    """
    Retorna o desempenho de todos os estudantes em uma disciplina específica.
    
    Args:
        disciplina: Nome da disciplina
        
    Returns:
        list: Lista de dicionários com dados de desempenho
    """
    con = conectar()
    cur = con.cursor()
    
    cur.execute("""
        SELECT nome, json_extract(desempenho_escolar, '$.' || ?)
        FROM estudantes
        WHERE json_extract(desempenho_escolar, '$.' || ?) IS NOT NULL
    """, (disciplina, disciplina))
    
    dados = []
    for nome, nota in cur.fetchall():
        dados.append({
            'estudante': nome,
            'nota': float(nota) if nota else 0.0
        })
    
    con.close()
    return dados

def obter_desempenho_estudante(estudante: str):
    """
    Retorna o desempenho de um estudante em todas as disciplinas.
    
    Args:
        estudante: Nome do estudante
        
    Returns:
        list: Lista de dicionários com dados de desempenho
    """
    con = conectar()
    cur = con.cursor()
    
    cur.execute("""
        SELECT desempenho_escolar
        FROM estudantes
        WHERE nome = ?
    """, (estudante,))
    
    row = cur.fetchone()
    if not row or not row[0]:
        return []
    
    desempenho = json.loads(row[0])
    dados = []
    for disciplina, nota in desempenho.items():
        dados.append({
            'disciplina': disciplina,
            'nota': float(nota) if nota else 0.0
        })
    
    con.close()
    return dados

def obter_recomendacoes():
    """
    Retorna as recomendações de carreira para todos os estudantes.
    
    Returns:
        list: Lista de dicionários com dados de recomendações
    """
    con = conectar()
    cur = con.cursor()
    
    cur.execute("""
        SELECT nome, json_extract(interesses, '$')
        FROM estudantes
        WHERE interesses IS NOT NULL
    """)
    
    dados = []
    for nome, interesses_json in cur.fetchall():
        if interesses_json:
            interesses = json.loads(interesses_json)
            for carreira in interesses:
                dados.append({
                    'estudante': nome,
                    'carreira': carreira
                })
    
    con.close()
    return dados

def excluir_estudante(nome):
    """
    Exclui um estudante do banco de dados pelo nome.
    
    Args:
        nome (str): Nome do estudante a ser excluído
        
    Returns:
        bool: True se o estudante foi excluído com sucesso, False caso contrário
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Verifica se o estudante existe
        cursor.execute("SELECT id FROM estudantes WHERE nome = ?", (nome,))
        estudante = cursor.fetchone()
        
        if not estudante:
            print(f"Estudante '{nome}' não encontrado no sistema.")
            return False
        
        # Exclui o estudante
        cursor.execute("DELETE FROM estudantes WHERE nome = ?", (nome,))
        conn.commit()
        
        return True
        
    except Exception as e:
        print(f"Erro ao excluir estudante: {str(e)}")
        return False
        
    finally:
        conn.close()

