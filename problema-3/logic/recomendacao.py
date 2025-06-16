from data.conexao import conectar
from data.transacao import executar_consulta, executar_comando, transacao

def salvar_recomendacao(estudante_id, carreira, score):
    """
    Salva uma recomendação de carreira para um estudante no banco de dados.
    """
    conn = conectar()
    try:
        with transacao(conn) as cursor:
            cursor.execute(
                "INSERT INTO recomendacoes (estudante_id, carreira, score) VALUES (?, ?, ?)",
                (estudante_id, carreira, score)
            )
    finally:
        conn.close()

def listar_recomendacoes():
    """
    Lista todas as recomendações feitas para todos os estudantes.
    """
    conn = conectar()
    try:
        return executar_consulta(conn, """
            SELECT estudante_id, carreira, score, data_recomendacao FROM recomendacoes
        """)
    finally:
        conn.close()

def cadastrar_regra(carreira: str, criterios: dict, peso: float = 1.0):
    """
    Cadastra uma nova regra de carreira no banco de dados.
    """
    conn = conectar()
    try:
        with transacao(conn) as cursor:
            # Verifica se já existe uma regra para essa carreira
            cursor.execute(
                "SELECT id FROM regras_carreira WHERE carreira = ?",
                (carreira,)
            )
            if cursor.fetchone():
                # Já existe, não insere novamente
                return
            # Insere a regra
            cursor.execute(
                "INSERT INTO regras_carreira (carreira, justificativa) VALUES (?, ?)",
                (carreira, criterios.get('justificativa', ''))
            )
            regra_id = cursor.lastrowid

            # Insere interesses
            for interesse in criterios.get('interesses', []):
                cursor.execute("SELECT id FROM interesses WHERE interesse = ?", (interesse,))
                row = cursor.fetchone()
                if row:
                    cursor.execute(
                        "INSERT INTO regras_interesses (regra_id, interesse_id) VALUES (?, ?)",
                        (regra_id, row[0])
                    )

            # Insere habilidades
            for habilidade in criterios.get('habilidades', []):
                cursor.execute("SELECT id FROM habilidades WHERE habilidade = ?", (habilidade,))
                row = cursor.fetchone()
                if row:
                    cursor.execute(
                        "INSERT INTO regras_habilidades (regra_id, habilidade_id) VALUES (?, ?)",
                        (regra_id, row[0])
                    )

            # Insere desempenho
            for disciplina, nota_min in criterios.get('desempenho', {}).items():
                cursor.execute("SELECT id FROM disciplinas WHERE disciplina = ?", (disciplina,))
                row = cursor.fetchone()
                if row:
                    cursor.execute(
                        "INSERT INTO regras_desempenho (regra_id, disciplina_id, nota_min, peso) VALUES (?, ?, ?, ?)",
                        (regra_id, row[0], nota_min, peso)
                    )
    finally:
        conn.close()

def listar_regras():
    """
    Lista todas as regras de carreira cadastradas.
    """
    conn = conectar()
    try:
        regras = []
        # Busca regras básicas
        rows = executar_consulta(conn, """
            SELECT DISTINCT rc.id, rc.carreira, rc.justificativa 
            FROM regras_carreira rc
            ORDER BY rc.carreira
        """)
        
        # Dicionário para controlar carreiras já processadas
        carreiras_processadas = {}
        
        for regra_id, carreira, justificativa in rows:
            # Se já processamos esta carreira, pula
            if carreira in carreiras_processadas:
                continue
                
            # Busca interesses
            interesses = executar_consulta(conn, """
                SELECT DISTINCT i.interesse FROM regras_interesses ri
                JOIN interesses i ON ri.interesse_id = i.id
                WHERE ri.regra_id = ?
                ORDER BY i.interesse
            """, (regra_id,))
            
            # Busca habilidades
            habilidades = executar_consulta(conn, """
                SELECT DISTINCT h.habilidade FROM regras_habilidades rh
                JOIN habilidades h ON rh.habilidade_id = h.id
                WHERE rh.regra_id = ?
                ORDER BY h.habilidade
            """, (regra_id,))
            
            # Busca desempenho
            desempenho = executar_consulta(conn, """
                SELECT DISTINCT d.disciplina, rd.nota_min, rd.peso FROM regras_desempenho rd
                JOIN disciplinas d ON rd.disciplina_id = d.id
                WHERE rd.regra_id = ?
                ORDER BY d.disciplina
            """, (regra_id,))
            
            # Organiza os dados no formato esperado pelo motor
            regra = {
                'id': regra_id,
                'carreira': carreira,
                'justificativa': justificativa,
                'condicoes': {
                    'interesses': [i[0] for i in interesses],
                    'habilidades': [h[0] for h in habilidades],
                    'desempenho': {d[0]: d[1] for d in desempenho},
                    'pesos': {d[0]: d[2] for d in desempenho}
                }
            }
            
            regras.append(regra)
            carreiras_processadas[carreira] = True
            
        return regras
    finally:
        conn.close()

def atualizar_peso_regra(regra_id: int, novo_peso: float):
    """
    Atualiza o peso de uma regra de carreira.
    """
    conn = conectar()
    try:
        executar_comando(conn, 
            "UPDATE regras_desempenho SET peso = ? WHERE regra_id = ?",
            (novo_peso, regra_id)
        )
    finally:
        conn.close()

def atualizar_regra(regra_id: int, regra: dict):
    """
    Atualiza uma regra de carreira existente.
    
    Args:
        regra_id: ID da regra a ser atualizada
        regra: Dicionário com os novos dados da regra
    """
    conn = conectar()
    try:
        with transacao(conn) as cursor:
            # Atualiza a regra básica
            cursor.execute(
                "UPDATE regras_carreira SET carreira = ?, justificativa = ? WHERE id = ?",
                (regra['carreira'], regra.get('justificativa', ''), regra_id)
            )

            # Remove dados antigos
            cursor.execute("DELETE FROM regras_interesses WHERE regra_id = ?", (regra_id,))
            cursor.execute("DELETE FROM regras_habilidades WHERE regra_id = ?", (regra_id,))
            cursor.execute("DELETE FROM regras_desempenho WHERE regra_id = ?", (regra_id,))

            # Insere novos interesses
            for interesse in regra['condicoes'].get('interesses', []):
                cursor.execute("SELECT id FROM interesses WHERE interesse = ?", (interesse,))
                row = cursor.fetchone()
                if row:
                    cursor.execute(
                        "INSERT INTO regras_interesses (regra_id, interesse_id) VALUES (?, ?)",
                        (regra_id, row[0])
                    )

            # Insere novas habilidades
            for habilidade in regra['condicoes'].get('habilidades', []):
                cursor.execute("SELECT id FROM habilidades WHERE habilidade = ?", (habilidade,))
                row = cursor.fetchone()
                if row:
                    cursor.execute(
                        "INSERT INTO regras_habilidades (regra_id, habilidade_id) VALUES (?, ?)",
                        (regra_id, row[0])
                    )

            # Insere novo desempenho
            for disciplina, nota_min in regra['condicoes'].get('desempenho', {}).items():
                cursor.execute("SELECT id FROM disciplinas WHERE disciplina = ?", (disciplina,))
                row = cursor.fetchone()
                if row:
                    peso = regra['condicoes'].get('pesos', {}).get(disciplina, 1.0)
                    cursor.execute(
                        "INSERT INTO regras_desempenho (regra_id, disciplina_id, nota_min, peso) VALUES (?, ?, ?, ?)",
                        (regra_id, row[0], nota_min, peso)
                    )
    finally:
        conn.close()

def remover_regra(regra_id: int):
    """
    Remove uma regra de carreira.
    
    Args:
        regra_id: ID da regra a ser removida
    """
    conn = conectar()
    try:
        with transacao(conn) as cursor:
            # Remove dados relacionados
            cursor.execute("DELETE FROM regras_interesses WHERE regra_id = ?", (regra_id,))
            cursor.execute("DELETE FROM regras_habilidades WHERE regra_id = ?", (regra_id,))
            cursor.execute("DELETE FROM regras_desempenho WHERE regra_id = ?", (regra_id,))
            
            # Remove a regra
            cursor.execute("DELETE FROM regras_carreira WHERE id = ?", (regra_id,))
    finally:
        conn.close()