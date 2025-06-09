"""
Módulo de acesso ao banco de dados para estudantes.

Responsável por criar a tabela, salvar e listar estudantes no banco SQLite.
"""
import json
from typing import List, Dict, Any, Optional, Tuple
from .conexao import conectar, desconectar
from .transacao import (
    executar_script,
    executar_consulta,
    executar_comando,
    verificar_tabela,
    verificar_coluna,
    TransacaoErro,
    ConsultaErro
)
from .validacao import (
    validar_estudante,
    ValidacaoErro
)
import sqlite3

def criar_tabela_estudantes() -> None:
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
    try:
        conexao = conectar()
        
        # Cria a tabela se não existir
        script = """
        CREATE TABLE IF NOT EXISTS estudantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            interesses TEXT,
            habilidades TEXT,
            desempenho_escolar TEXT,
            recomendacoes TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        executar_script(conexao, script)
        
        # Verifica e adiciona colunas se necessário
        if not verificar_coluna(conexao, 'estudantes', 'habilidades'):
            executar_script(conexao, "ALTER TABLE estudantes ADD COLUMN habilidades TEXT")
        
        if not verificar_coluna(conexao, 'estudantes', 'desempenho_escolar'):
            executar_script(conexao, "ALTER TABLE estudantes ADD COLUMN desempenho_escolar TEXT")
        
        if not verificar_coluna(conexao, 'estudantes', 'data_criacao'):
            executar_script(conexao, "ALTER TABLE estudantes ADD COLUMN data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        
        if not verificar_coluna(conexao, 'estudantes', 'data_atualizacao'):
            executar_script(conexao, "ALTER TABLE estudantes ADD COLUMN data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        
    except Exception as e:
        raise ConsultaErro(f"Erro ao criar tabela de estudantes: {str(e)}")
    finally:
        desconectar()

def salvar_estudante(estudante: Dict[str, Any]) -> int:
    """
    Salva um estudante no banco de dados.

    Args:
        estudante: Dicionário com os dados do estudante

    Returns:
        ID do estudante salvo

    Raises:
        ValidacaoErro: Se os dados do estudante forem inválidos
        ConsultaErro: Se ocorrer erro ao salvar no banco
    """
    try:
        # Valida e sanitiza os dados
        nome, interesses, habilidades, desempenho = validar_estudante(estudante)
        
        # Converte para JSON
        interesses_json = json.dumps(interesses)
        habilidades_json = json.dumps(habilidades)
        desempenho_json = json.dumps(desempenho)
        
        conexao = conectar()
        
        # Verifica se o estudante já existe
        query = "SELECT id FROM estudantes WHERE nome = ?"
        resultado = executar_consulta(conexao, query, (nome,))
        
        if resultado:
            # Atualiza estudante existente
            query = """
            UPDATE estudantes 
            SET interesses = ?, habilidades = ?, desempenho_escolar = ?, data_atualizacao = CURRENT_TIMESTAMP
            WHERE nome = ?
            """
            executar_comando(conexao, query, (interesses_json, habilidades_json, desempenho_json, nome))
            return resultado[0][0]
        else:
            # Insere novo estudante
            query = """
            INSERT INTO estudantes (nome, interesses, habilidades, desempenho_escolar)
            VALUES (?, ?, ?, ?)
            """
            executar_comando(conexao, query, (nome, interesses_json, habilidades_json, desempenho_json))
            
            # Obtém o ID do estudante inserido
            query = "SELECT last_insert_rowid()"
            resultado = executar_consulta(conexao, query)
            return resultado[0][0]
            
    except ValidacaoErro as e:
        raise e
    except Exception as e:
        raise ConsultaErro(f"Erro ao salvar estudante: {str(e)}")
    finally:
        desconectar()

def listar_estudantes() -> List[Tuple[int, str, List[str], List[str], Dict[str, float]]]:
    """
    Retorna todos os estudantes cadastrados no banco de dados.

    Returns:
        Lista de tuplas contendo (id, nome, interesses, habilidades, desempenho_escolar)

    Raises:
        ConsultaErro: Se ocorrer erro ao listar estudantes
    """
    try:
        conexao = conectar()
        
        query = """
        SELECT id, nome, interesses, habilidades, desempenho_escolar 
        FROM estudantes
        ORDER BY nome
        """
        rows = executar_consulta(conexao, query)
        
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
        
        return estudantes
        
    except Exception as e:
        raise ConsultaErro(f"Erro ao listar estudantes: {str(e)}")
    finally:
        desconectar()

def buscar_estudante(nome: str) -> Optional[Tuple[int, str, List[str], List[str], Dict[str, float]]]:
    """
    Busca um estudante pelo nome.

    Args:
        nome: Nome do estudante a ser buscado

    Returns:
        Tupla com dados do estudante ou None se não encontrado

    Raises:
        ConsultaErro: Se ocorrer erro ao buscar estudante
    """
    try:
        conexao = conectar()
        
        query = """
        SELECT id, nome, interesses, habilidades, desempenho_escolar
        FROM estudantes
        WHERE nome = ?
        """
        resultado = executar_consulta(conexao, query, (nome,))
        
        if not resultado:
            return None
        
        id_, nome, interesses_json, habilidades_json, desempenho_json = resultado[0]
        
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
        
        return (id_, nome, interesses, habilidades, desempenho)
        
    except Exception as e:
        raise ConsultaErro(f"Erro ao buscar estudante: {str(e)}")
    finally:
        desconectar()

def excluir_estudante(nome: str) -> bool:
    """
    Exclui um estudante do banco de dados pelo nome.
    
    Args:
        nome: Nome do estudante a ser excluído
        
    Returns:
        True se o estudante foi excluído com sucesso, False caso contrário
        
    Raises:
        ConsultaErro: Se ocorrer erro ao excluir estudante
    """
    try:
        conexao = conectar()
        
        # Verifica se o estudante existe
        query = "SELECT id FROM estudantes WHERE nome = ?"
        resultado = executar_consulta(conexao, query, (nome,))
        
        if not resultado:
            return False
        
        # Exclui o estudante
        query = "DELETE FROM estudantes WHERE nome = ?"
        executar_comando(conexao, query, (nome,))
        
        return True
        
    except Exception as e:
        raise ConsultaErro(f"Erro ao excluir estudante: {str(e)}")
    finally:
        desconectar()

def obter_disciplinas() -> List[str]:
    """
    Retorna a lista de todas as disciplinas registradas no banco.
    
    Returns:
        Lista de nomes de disciplinas
        
    Raises:
        ConsultaErro: Se ocorrer erro ao obter disciplinas
    """
    try:
        conexao = conectar()
        
        query = "SELECT DISTINCT json_extract(desempenho_escolar, '$.*') FROM estudantes"
        resultado = executar_consulta(conexao, query)
        
        disciplinas = set()
        for row in resultado:
            if row[0]:
                try:
                    desempenho = json.loads(row[0])
                    disciplinas.update(desempenho.keys())
                except Exception:
                    continue
        
        return sorted(list(disciplinas))
        
    except Exception as e:
        raise ConsultaErro(f"Erro ao obter disciplinas: {str(e)}")
    finally:
        desconectar()

def obter_desempenho_disciplina(disciplina: str) -> List[Dict[str, Any]]:
    """
    Retorna o desempenho de todos os estudantes em uma disciplina específica.
    
    Args:
        disciplina: Nome da disciplina
        
    Returns:
        Lista de dicionários com dados de desempenho
        
    Raises:
        ConsultaErro: Se ocorrer erro ao obter desempenho
    """
    try:
        conexao = conectar()
        
        query = """
        SELECT nome, json_extract(desempenho_escolar, '$.' || ?)
        FROM estudantes
        WHERE json_extract(desempenho_escolar, '$.' || ?) IS NOT NULL
        """
        resultado = executar_consulta(conexao, query, (disciplina, disciplina))
        
        dados = []
        for nome, nota in resultado:
            try:
                nota = float(nota) if nota else 0.0
                dados.append({
                    'estudante': nome,
                    'nota': nota
                })
            except Exception:
                continue
        
        return dados
        
    except Exception as e:
        raise ConsultaErro(f"Erro ao obter desempenho da disciplina: {str(e)}")
    finally:
        desconectar()

def obter_desempenho_estudante(estudante: str) -> List[Dict[str, Any]]:
    """
    Retorna o desempenho de um estudante em todas as disciplinas.
    
    Args:
        estudante: Nome do estudante
        
    Returns:
        Lista de dicionários com dados de desempenho
        
    Raises:
        ConsultaErro: Se ocorrer erro ao obter desempenho
    """
    try:
        conexao = conectar()
        
        query = """
        SELECT desempenho_escolar
        FROM estudantes
        WHERE nome = ?
        """
        resultado = executar_consulta(conexao, query, (estudante,))
        
        if not resultado or not resultado[0][0]:
            return []
        
        try:
            desempenho = json.loads(resultado[0][0])
            dados = []
            for disciplina, nota in desempenho.items():
                try:
                    nota = float(nota) if nota else 0.0
                    dados.append({
                        'disciplina': disciplina,
                        'nota': nota
                    })
                except Exception:
                    continue
            return dados
        except Exception:
            return []
        
    except Exception as e:
        raise ConsultaErro(f"Erro ao obter desempenho do estudante: {str(e)}")
    finally:
        desconectar()

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

def buscar_estudante_por_nome(nome: str) -> Optional[Tuple[int, str, List[str], List[str], Dict[str, float]]]:
    """
    Busca um estudante pelo nome.
    
    Args:
        nome: Nome do estudante a ser buscado
        
    Returns:
        Tupla com os dados do estudante (id, nome, interesses, habilidades, desempenho)
        ou None se não encontrado
        
    Raises:
        ConsultaErro: Se ocorrer erro ao buscar o estudante
    """
    try:
        conexao = conectar()
        
        query = """
        SELECT id, nome, interesses, habilidades, desempenho_escolar
        FROM estudantes
        WHERE LOWER(nome) LIKE LOWER(?)
        """
        resultado = executar_consulta(conexao, query, (f"%{nome}%",))
        
        if not resultado:
            return None
        
        id_, nome, interesses_json, habilidades_json, desempenho_json = resultado[0]
        
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
        
        return (id_, nome, interesses, habilidades, desempenho)
        
    except Exception as e:
        raise ConsultaErro(f"Erro ao buscar estudante: {str(e)}")
    finally:
        desconectar()

def obter_desempenho_por_disciplina(disciplina: str) -> List[Tuple[str, float]]:
    """
    Retorna o desempenho de todos os estudantes em uma disciplina específica.
    
    Args:
        disciplina: Nome da disciplina
        
    Returns:
        Lista de tuplas (nome_estudante, nota)
        
    Raises:
        ConsultaErro: Se ocorrer erro ao obter os dados
    """
    try:
        conexao = conectar()
        
        query = """
        SELECT nome, json_extract(desempenho_escolar, '$.' || ?)
        FROM estudantes
        WHERE json_extract(desempenho_escolar, '$.' || ?) IS NOT NULL
        """
        resultado = executar_consulta(conexao, query, (disciplina, disciplina))
        
        desempenhos = []
        for nome, nota in resultado:
            try:
                nota = float(nota) if nota else 0.0
                desempenhos.append((nome, nota))
            except Exception:
                continue
        
        return desempenhos
        
    except Exception as e:
        raise ConsultaErro(f"Erro ao obter desempenho por disciplina: {str(e)}")
    finally:
        desconectar()

def obter_desempenho_por_estudante(estudante: str) -> List[Tuple[str, float]]:
    """
    Retorna o desempenho de um estudante em todas as disciplinas.
    
    Args:
        estudante: Nome do estudante
        
    Returns:
        Lista de tuplas (disciplina, nota)
        
    Raises:
        ConsultaErro: Se ocorrer erro ao obter os dados
    """
    try:
        conexao = conectar()
        
        query = """
        SELECT desempenho_escolar
        FROM estudantes
        WHERE nome = ?
        """
        resultado = executar_consulta(conexao, query, (estudante,))
        
        if not resultado or not resultado[0][0]:
            return []
        
        try:
            desempenho = json.loads(resultado[0][0])
            return [(disciplina, float(nota)) for disciplina, nota in desempenho.items()]
        except Exception:
            return []
        
    except Exception as e:
        raise ConsultaErro(f"Erro ao obter desempenho por estudante: {str(e)}")
    finally:
        desconectar()

def atualizar_recomendacoes(estudante_id: int, recomendacoes: Dict[str, Any]) -> None:
    """
    Atualiza as recomendações de carreira de um estudante.
    
    Args:
        estudante_id: ID do estudante
        recomendacoes: Dicionário com as recomendações (recomendadas e próximas)
        
    Raises:
        ConsultaErro: Se houver erro ao atualizar as recomendações
    """
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                UPDATE estudantes 
                SET recomendacoes = ? 
                WHERE id = ?
            """, (json.dumps(recomendacoes), estudante_id))
            conexao.commit()
    except sqlite3.Error as e:
        raise ConsultaErro(f"Erro ao atualizar recomendações: {str(e)}")

def inicializar_banco():
    """
    Inicializa o banco de dados criando a tabela de estudantes se ela não existir
    e adiciona a coluna de recomendações se necessário.
    """
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            
            # Cria a tabela se não existir
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS estudantes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    interesses TEXT NOT NULL,
                    habilidades TEXT NOT NULL,
                    desempenho TEXT NOT NULL,
                    recomendacoes TEXT
                )
            """)
            
            # Verifica se a coluna recomendacoes existe
            cursor.execute("PRAGMA table_info(estudantes)")
            colunas = [coluna[1] for coluna in cursor.fetchall()]
            
            # Se a coluna não existir, adiciona ela
            if 'recomendacoes' not in colunas:
                cursor.execute("ALTER TABLE estudantes ADD COLUMN recomendacoes TEXT")
            
            conexao.commit()
    except sqlite3.Error as e:
        raise ConsultaErro(f"Erro ao inicializar banco de dados: {str(e)}")

