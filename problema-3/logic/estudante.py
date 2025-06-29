from data.conexao import conectar
from data.transacao import executar_consulta, executar_comando, transacao
from logic.recomendacao import salvar_recomendacao

def exibir_estudantes(estudantes):
    if not estudantes:
        print("\nNenhum estudante cadastrado.")
        return
    print("\n=== Estudantes Cadastrados ===")
    for est in estudantes:
        print(f"ID: {est[0]} | Nome: {est[1]}")

def buscar_estudante():
    """
    Busca um estudante pelo nome e exibe seus dados completos.
    """
    from utils.interface import Interface  # Importação movida para dentro da função
    
    nome = input("\nDigite o nome do estudante: ").strip()
    estudantes = listar_estudantes()
    encontrados = [est for est in estudantes if nome.lower() in est[1].lower()]
    
    if not encontrados:
        print("\nNenhum estudante encontrado com esse nome.")
        return
    
    print("\n=== Estudantes Encontrados ===")
    for estudante in encontrados:
        Interface.exibir_dados_estudante(estudante)
        print()  # Linha em branco entre estudantes

def coletar_opcoes(lista, titulo):
    """
    Exibe uma lista numerada e permite ao usuário selecionar opções por número.
    Retorna uma lista com os itens selecionados.
    """
    if not lista:
        print(f"\nNenhuma opção disponível para {titulo}.")
        return []
    print(f"\nSelecione {titulo} (digite os números separados por vírgula, ENTER para finalizar):")
    for idx, item in enumerate(lista, 1):
        print(f"{idx}. {item}")
    while True:
        entrada = input("Números: ").strip()
        if not entrada:
            return []
        try:
            indices = [int(i.strip()) for i in entrada.split(',')]
            selecionados = [lista[i-1] for i in indices if 1 <= i <= len(lista)]
            if selecionados:
                return selecionados
            else:
                print("Selecione pelo menos um número válido.")
        except Exception:
            print("Entrada inválida. Digite apenas números separados por vírgula.")

def coletar_dados_estudante():
    """
    Coleta os dados do estudante via terminal, buscando opções no banco de dados.
    """
    nome = input("\nNome do estudante: ").strip()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT interesse FROM interesses")
    interesses_disp = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT habilidade FROM habilidades")
    habilidades_disp = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT disciplina FROM disciplinas")
    disciplinas_disp = [row[0] for row in cursor.fetchall()]
    conn.close()

    interesses = coletar_opcoes(interesses_disp, "os interesses")
    habilidades = coletar_opcoes(habilidades_disp, "as habilidades")
    desempenho = {}
    print("\nInforme as notas do estudante nas disciplinas (digite o número da disciplina e a nota, ENTER para finalizar):")
    for idx, disciplina in enumerate(disciplinas_disp, 1):
        print(f"{idx}. {disciplina}")
    while True:
        entrada = input("Número da disciplina (ou ENTER para finalizar): ").strip()
        if not entrada:
            break
        try:
            num = int(entrada)
            if 1 <= num <= len(disciplinas_disp):
                nome_disc = disciplinas_disp[num-1]
                nota = float(input(f"Nota em {nome_disc}: "))
                if 0 <= nota <= 10:
                    desempenho[nome_disc] = nota
                else:
                    print("Nota fora do intervalo 0-10. Ignorada.")
            else:
                print("Número de disciplina inválido.")
        except ValueError:
            print("Entrada inválida. Digite apenas o número da disciplina.")

    return {
        'nome': nome,
        'interesses': interesses,
        'habilidades': habilidades,
        'desempenho': desempenho
    }

def salvar_estudante(estudante):
    """
    Salva um estudante e seus relacionamentos nas tabelas intermediárias do banco de dados.
    
    Returns:
        int: ID do estudante cadastrado
    """
    conn = conectar()
    try:
        with transacao(conn) as cursor:
            # Verifica se já existe um estudante com o mesmo nome
            cursor.execute("SELECT id FROM estudantes WHERE LOWER(nome) = ?", (estudante['nome'].lower(),))
            existing = cursor.fetchone()
            if existing:
                raise ValueError(f"Já existe um estudante cadastrado com o nome '{estudante['nome']}'")

            # 1. Salva o estudante (apenas nome)
            cursor.execute(
                "INSERT INTO estudantes (nome) VALUES (?)",
                (estudante['nome'],)
            )
            estudante_id = cursor.lastrowid

            # 2. Salva interesses
            for interesse in estudante['interesses']:
                cursor.execute("SELECT id FROM interesses WHERE interesse = ?", (interesse,))
                row = cursor.fetchone()
                if row:
                    interesse_id = row[0]
                    cursor.execute(
                        "INSERT INTO estudantes_interesses (estudante_id, interesse_id) VALUES (?, ?)",
                        (estudante_id, interesse_id)
                    )

            # 3. Salva habilidades
            for habilidade in estudante['habilidades']:
                cursor.execute("SELECT id FROM habilidades WHERE habilidade = ?", (habilidade,))
                row = cursor.fetchone()
                if row:
                    habilidade_id = row[0]
                    cursor.execute(
                        "INSERT INTO estudantes_habilidades (estudante_id, habilidade_id) VALUES (?, ?)",
                        (estudante_id, habilidade_id)
                    )

            # 4. Salva desempenho
            for disciplina, nota in estudante['desempenho'].items():
                cursor.execute("SELECT id FROM disciplinas WHERE disciplina = ?", (disciplina,))
                row = cursor.fetchone()
                if row:
                    disciplina_id = row[0]
                    cursor.execute(
                        "INSERT INTO desempenho_estudante (estudante_id, disciplina_id, nota) VALUES (?, ?, ?)",
                        (estudante_id, disciplina_id, nota)
                    )
            
            return estudante_id
    finally:
        conn.close()

def cadastrar_estudante():
    """
    Executa o fluxo de cadastro de um novo estudante.
    """
    try:
        estudante = coletar_dados_estudante()
        salvar_estudante(estudante)
        print("\nEstudante cadastrado com sucesso!\n")
    except Exception as e:
        print(f"\nErro ao cadastrar estudante: {str(e)}")

def listar_estudantes():
    """
    Retorna uma lista de tuplas com todos os dados dos estudantes (id, nome, interesses, habilidades, desempenho).
    """
    conn = conectar()
    try:
        estudantes = []
        # Busca estudantes básicos
        rows = executar_consulta(conn, "SELECT id, nome FROM estudantes ORDER BY id ASC")
        
        for estudante_id, nome in rows:
            # Busca interesses
            interesses_rows = executar_consulta(conn, """
                SELECT i.interesse FROM estudantes_interesses ie
                JOIN interesses i ON ie.interesse_id = i.id
                WHERE ie.estudante_id = ?
            """, (estudante_id,))
            interesses = [r[0] for r in interesses_rows]
            
            # Busca habilidades
            habilidades_rows = executar_consulta(conn, """
                SELECT h.habilidade FROM estudantes_habilidades he
                JOIN habilidades h ON he.habilidade_id = h.id
                WHERE he.estudante_id = ?
            """, (estudante_id,))
            habilidades = [r[0] for r in habilidades_rows]
            
            # Busca desempenho
            desempenho_rows = executar_consulta(conn, """
                SELECT d.disciplina, de.nota FROM desempenho_estudante de
                JOIN disciplinas d ON de.disciplina_id = d.id
                WHERE de.estudante_id = ?
            """, (estudante_id,))
            desempenho = {disciplina: nota for disciplina, nota in desempenho_rows}
            
            estudantes.append((estudante_id, nome, interesses, habilidades, desempenho))
        
        return estudantes
    finally:
        conn.close()

def buscar_estudante_completo_por_nome(nome):
    """
    Retorna uma tupla com todos os dados do estudante (id, nome, interesses, habilidades, desempenho)
    a partir das tabelas intermediárias, buscando pelo nome exato.
    """
    conn = conectar()
    try:
        # Buscar estudante
        rows = executar_consulta(conn, "SELECT id, nome FROM estudantes WHERE LOWER(nome) = ?", (nome.lower(),))
        if not rows:
            return None
        estudante_id, nome = rows[0]

        # Buscar interesses
        rows = executar_consulta(conn, """
            SELECT i.interesse FROM estudantes_interesses ie
            JOIN interesses i ON ie.interesse_id = i.id
            WHERE ie.estudante_id = ?
        """, (estudante_id,))
        interesses = [r[0] for r in rows]

        # Buscar habilidades
        rows = executar_consulta(conn, """
            SELECT h.habilidade FROM estudantes_habilidades he
            JOIN habilidades h ON he.habilidade_id = h.id
            WHERE he.estudante_id = ?
        """, (estudante_id,))
        habilidades = [r[0] for r in rows]

        # Buscar desempenho
        rows = executar_consulta(conn, """
            SELECT d.disciplina, de.nota FROM desempenho_estudante de
            JOIN disciplinas d ON de.disciplina_id = d.id
            WHERE de.estudante_id = ?
        """, (estudante_id,))
        desempenho = {disciplina: nota for disciplina, nota in rows}

        return (estudante_id, nome, interesses, habilidades, desempenho)
    finally:
        conn.close()

def recomendar_carreiras(estudante_id, interesses, habilidades, desempenho):
    """
    Gera recomendações de carreiras para um estudante com base em seus interesses,
    habilidades e desempenho escolar.
    """
    # Exemplo simplificado de lógica de recomendação
    recomendacoes = []
    if 'programação' in habilidades or 'lógica' in interesses:
        recomendacoes.append({'carreira': 'Desenvolvedor de Software', 'score': 90})
    if 'design' in habilidades or 'criatividade' in interesses:
        recomendacoes.append({'carreira': 'Designer Gráfico', 'score': 85})
    if 'matemática' in habilidades or 'análise' in interesses:
        recomendacoes.append({'carreira': 'Analista de Dados', 'score': 88})
    if 'comunicação' in habilidades or 'persuasão' in interesses:
        recomendacoes.append({'carreira': 'Marketing', 'score': 80})

    # Ordenar recomendações por score (maior para menor)
    recomendacoes = sorted(recomendacoes, key=lambda x: x['score'], reverse=True)

    # Salvar recomendações no banco de dados
    for rec in recomendacoes:
        salvar_recomendacao(estudante_id, rec['carreira'], rec['score'])

    return recomendacoes