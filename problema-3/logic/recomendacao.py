from data.conexao import conectar
from data.transacao import executar_consulta, executar_comando, transacao
from data.validacao import validar_regra, ValidacaoErro
from typing import List, Dict, Any

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

def cadastrar_regra(regra: dict) -> int:
    """
    Cadastra uma nova regra de carreira.
    
    Args:
        regra: Dicionário com dados da regra
        
    Returns:
        ID da regra cadastrada
        
    Raises:
        ValidacaoErro: Se os dados forem inválidos
    """
    # Valida os dados
    carreira, justificativa, interesses, habilidades, desempenho = validar_regra(regra)
    
    conn = conectar()
    try:
        with transacao(conn) as cursor:
            # Verifica se já existe uma regra para esta carreira
            cursor.execute("SELECT id FROM regras_carreira WHERE LOWER(carreira) = ?", (carreira,))
            if cursor.fetchone():
                raise ValidacaoErro(f"Já existe uma regra cadastrada para a carreira '{carreira}'")
            
            # Insere a regra
            cursor.execute(
                "INSERT INTO regras_carreira (carreira, justificativa) VALUES (?, ?)",
                (carreira, justificativa)
            )
            regra_id = cursor.lastrowid
            
            # Insere interesses
            for interesse in interesses:
                cursor.execute("SELECT id FROM interesses WHERE interesse = ?", (interesse,))
                row = cursor.fetchone()
                if row:
                    interesse_id = row[0]
                    cursor.execute(
                        "INSERT INTO regras_interesses (regra_id, interesse_id) VALUES (?, ?)",
                        (regra_id, interesse_id)
                    )
            
            # Insere habilidades
            for habilidade in habilidades:
                cursor.execute("SELECT id FROM habilidades WHERE habilidade = ?", (habilidade,))
                row = cursor.fetchone()
                if row:
                    habilidade_id = row[0]
                    cursor.execute(
                        "INSERT INTO regras_habilidades (regra_id, habilidade_id) VALUES (?, ?)",
                        (regra_id, habilidade_id)
                    )
            
            # Insere desempenho
            for disciplina, nota in desempenho.items():
                cursor.execute("SELECT id FROM disciplinas WHERE disciplina = ?", (disciplina,))
                row = cursor.fetchone()
                if row:
                    disciplina_id = row[0]
                    cursor.execute(
                        "INSERT INTO regras_desempenho (regra_id, disciplina_id, nota_min) VALUES (?, ?, ?)",
                        (regra_id, disciplina_id, nota)
                    )
            
            return regra_id
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

def editar_regra(regra_id: int, regra: dict):
    """
    Edita uma regra de carreira existente.
    
    Args:
        regra_id: ID da regra a ser editada
        regra: Dicionário com novos dados da regra
        
    Raises:
        ValidacaoErro: Se os dados forem inválidos
    """
    # Valida os dados
    carreira, justificativa, interesses, habilidades, desempenho = validar_regra(regra)
    
    conn = conectar()
    try:
        with transacao(conn) as cursor:
            # Verifica se a regra existe
            cursor.execute("SELECT id FROM regras_carreira WHERE id = ?", (regra_id,))
            if not cursor.fetchone():
                raise ValidacaoErro(f"Regra com ID {regra_id} não encontrada")
            
            # Verifica se já existe outra regra com o mesmo nome
            cursor.execute(
                "SELECT id FROM regras_carreira WHERE LOWER(carreira) = ? AND id != ?",
                (carreira, regra_id)
            )
            if cursor.fetchone():
                raise ValidacaoErro(f"Já existe uma regra cadastrada para a carreira '{carreira}'")
            
            # Atualiza a regra
            cursor.execute(
                "UPDATE regras_carreira SET carreira = ?, justificativa = ? WHERE id = ?",
                (carreira, justificativa, regra_id)
            )
            
            # Remove dados antigos
            cursor.execute("DELETE FROM regras_interesses WHERE regra_id = ?", (regra_id,))
            cursor.execute("DELETE FROM regras_habilidades WHERE regra_id = ?", (regra_id,))
            cursor.execute("DELETE FROM regras_desempenho WHERE regra_id = ?", (regra_id,))
            
            # Insere novos interesses
            for interesse in interesses:
                cursor.execute("SELECT id FROM interesses WHERE interesse = ?", (interesse,))
                row = cursor.fetchone()
                if row:
                    interesse_id = row[0]
                    cursor.execute(
                        "INSERT INTO regras_interesses (regra_id, interesse_id) VALUES (?, ?)",
                        (regra_id, interesse_id)
                    )
            
            # Insere novas habilidades
            for habilidade in habilidades:
                cursor.execute("SELECT id FROM habilidades WHERE habilidade = ?", (habilidade,))
                row = cursor.fetchone()
                if row:
                    habilidade_id = row[0]
                    cursor.execute(
                        "INSERT INTO regras_habilidades (regra_id, habilidade_id) VALUES (?, ?)",
                        (regra_id, habilidade_id)
                    )
            
            # Insere novo desempenho
            for disciplina, nota in desempenho.items():
                cursor.execute("SELECT id FROM disciplinas WHERE disciplina = ?", (disciplina,))
                row = cursor.fetchone()
                if row:
                    disciplina_id = row[0]
                    cursor.execute(
                        "INSERT INTO regras_desempenho (regra_id, disciplina_id, nota_min) VALUES (?, ?, ?)",
                        (regra_id, disciplina_id, nota)
                    )
    finally:
        conn.close()

def listar_recomendacoes(estudante_id: int) -> list:
    """
    Lista as recomendações de carreira para um estudante.
    
    Args:
        estudante_id: ID do estudante
        
    Returns:
        Lista de dicionários com dados das recomendações
    """
    conn = conectar()
    try:
        return executar_consulta(conn, """
            SELECT r.carreira, r.justificativa, rec.score
            FROM recomendacoes rec
            JOIN regras_carreira r ON rec.regra_id = r.id
            WHERE rec.estudante_id = ?
            ORDER BY rec.score DESC
        """, (estudante_id,))
    finally:
        conn.close()

def gerar_recomendacoes(estudante_id: int) -> list:
    """
    Gera recomendações de carreira para um estudante.
    
    Args:
        estudante_id: ID do estudante
        
    Returns:
        Lista de dicionários com dados das recomendações
    """
    conn = conectar()
    try:
        # Busca dados do estudante
        estudante = executar_consulta(conn, """
            SELECT e.nome, 
                   GROUP_CONCAT(i.interesse) as interesses,
                   GROUP_CONCAT(h.habilidade) as habilidades,
                   GROUP_CONCAT(d.disciplina || ':' || de.nota) as desempenho
            FROM estudantes e
            LEFT JOIN estudantes_interesses ei ON e.id = ei.estudante_id
            LEFT JOIN interesses i ON ei.interesse_id = i.id
            LEFT JOIN estudantes_habilidades eh ON e.id = eh.estudante_id
            LEFT JOIN habilidades h ON eh.habilidade_id = h.id
            LEFT JOIN desempenho_estudante de ON e.id = de.estudante_id
            LEFT JOIN disciplinas d ON de.disciplina_id = d.id
            WHERE e.id = ?
            GROUP BY e.id
        """, (estudante_id,))
        
        if not estudante:
            raise ValidacaoErro(f"Estudante com ID {estudante_id} não encontrado")
        
        # Extrai os dados do estudante da tupla retornada
        nome, interesses_str, habilidades_str, desempenho_str = estudante[0]
        
        # Processa os dados
        interesses = interesses_str.split(',') if interesses_str else []
        habilidades = habilidades_str.split(',') if habilidades_str else []
        desempenho = {}
        if desempenho_str:
            for item in desempenho_str.split(','):
                disciplina, nota = item.split(':')
                desempenho[disciplina] = float(nota)
        
        # Busca regras
        regras = listar_regras()
        recomendacoes = []
        
        for regra in regras:
            regra_id = regra['id']
            carreira = regra['carreira']
            justificativa = regra['justificativa']
            regra_interesses = regra['condicoes']['interesses']
            regra_habilidades = regra['condicoes']['habilidades']
            regra_desempenho = regra['condicoes']['desempenho']
            
            # Calcula score baseado em interesses
            score_interesses = sum(1 for i in interesses if i in regra_interesses) / len(regra_interesses) if regra_interesses else 0
            
            # Calcula score baseado em habilidades
            score_habilidades = sum(1 for h in habilidades if h in regra_habilidades) / len(regra_habilidades) if regra_habilidades else 0
            
            # Calcula score baseado em desempenho
            score_desempenho = 0
            if regra_desempenho and desempenho:
                notas = []
                for disciplina, nota_minima in regra_desempenho.items():
                    if disciplina in desempenho:
                        nota_estudante = desempenho[disciplina]
                        if nota_estudante >= nota_minima:
                            notas.append(1)
                        else:
                            notas.append(nota_estudante / nota_minima)
                score_desempenho = sum(notas) / len(notas) if notas else 0
            
            # Calcula score final (média ponderada)
            score_final = (score_interesses * 0.4 + score_habilidades * 0.3 + score_desempenho * 0.3) * 100
            
            if score_final >= 60:  # Só recomenda se o score for >= 60%
                recomendacoes.append({
                    'regra_id': regra_id,
                    'carreira': carreira,
                    'justificativa': justificativa,
                    'score': score_final
                })
        
        # Ordena recomendações por score
        recomendacoes.sort(key=lambda x: x['score'], reverse=True)
        
        # Salva recomendações
        with transacao(conn) as cursor:
            cursor.execute("DELETE FROM recomendacoes WHERE estudante_id = ?", (estudante_id,))
            for rec in recomendacoes:
                cursor.execute(
                    "INSERT INTO recomendacoes (estudante_id, regra_id, score) VALUES (?, ?, ?)",
                    (estudante_id, rec['regra_id'], rec['score'])
                )
        
        return recomendacoes
    finally:
        conn.close()

def listar_todas_recomendacoes() -> List[Dict[str, Any]]:
    """
    Lista todas as recomendações de carreira para todos os estudantes.
    
    Returns:
        List[Dict[str, Any]]: Lista de dicionários com dados das recomendações
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Busca todas as recomendações
        cursor.execute("""
            SELECT e.nome, rec.carreira, rec.score
            FROM estudantes e
            JOIN recomendacoes rec ON e.id = rec.estudante_id
            ORDER BY rec.score DESC
        """)
        
        recomendacoes = []
        for nome, carreira, score in cursor.fetchall():
            recomendacoes.append({
                'estudante': nome,
                'carreira': carreira,
                'score': score
            })
            
        return recomendacoes
        
    except Exception as e:
        raise Exception(f"Erro ao listar recomendações: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()