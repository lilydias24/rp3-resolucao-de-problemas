from data.conexao import conectar
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
    Busca um estudante pelo nome.
    """
    nome = input("\nDigite o nome do estudante: ").strip()
    estudantes = listar_estudantes()
    encontrados = [est for est in estudantes if nome.lower() in est[1].lower()]
    exibir_estudantes(encontrados)

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
        'desempenho_escolar': desempenho
    }

def salvar_estudante(estudante):
    """
    Salva um estudante e seus relacionamentos nas tabelas intermediárias do banco de dados.
    """
    conn = conectar()
    cursor = conn.cursor()
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
                "INSERT INTO interesses_estudante (estudante_id, interesse_id) VALUES (?, ?)",
                (estudante_id, interesse_id)
            )

    # 3. Salva habilidades
    for habilidade in estudante['habilidades']:
        cursor.execute("SELECT id FROM habilidades WHERE habilidade = ?", (habilidade,))
        row = cursor.fetchone()
        if row:
            habilidade_id = row[0]
            cursor.execute(
                "INSERT INTO habilidades_estudante (estudante_id, habilidade_id) VALUES (?, ?)",
                (estudante_id, habilidade_id)
            )

    # 4. Salva desempenho
    for disciplina, nota in estudante['desempenho_escolar'].items():
        cursor.execute("SELECT id FROM disciplinas WHERE disciplina = ?", (disciplina,))
        row = cursor.fetchone()
        if row:
            disciplina_id = row[0]
            cursor.execute(
                "INSERT INTO desempenho_estudante (estudante_id, disciplina_id, nota) VALUES (?, ?, ?)",
                (estudante_id, disciplina_id, nota)
            )

    conn.commit()
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
    Retorna uma lista de tuplas (id, nome) de todos os estudantes cadastrados, ordenados por ID.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM estudantes ORDER BY id ASC")
    estudantes = cursor.fetchall()
    conn.close()
    return estudantes

def buscar_estudante_completo_por_nome(nome):
    """
    Retorna um dicionário com todos os dados do estudante (nome, interesses, habilidades, desempenho)
    a partir das tabelas intermediárias, buscando pelo nome exato.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM estudantes WHERE LOWER(nome) = ?", (nome.lower(),))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    estudante_id, nome = row

    # Buscar interesses
    cursor.execute("""
        SELECT i.interesse FROM interesses_estudante ie
        JOIN interesses i ON ie.interesse_id = i.id
        WHERE ie.estudante_id = ?
    """, (estudante_id,))
    interesses = [r[0] for r in cursor.fetchall()]

    # Buscar habilidades
    cursor.execute("""
        SELECT h.habilidade FROM habilidades_estudante he
        JOIN habilidades h ON he.habilidade_id = h.id
        WHERE he.estudante_id = ?
    """, (estudante_id,))
    habilidades = [r[0] for r in cursor.fetchall()]

    # Buscar desempenho
    cursor.execute("""
        SELECT d.disciplina, de.nota FROM desempenho_estudante de
        JOIN disciplinas d ON de.disciplina_id = d.id
        WHERE de.estudante_id = ?
    """, (estudante_id,))
    desempenho = {disciplina: nota for disciplina, nota in cursor.fetchall()}

    conn.close()
    return {
        'nome': nome,
        'interesses': interesses,
        'habilidades': habilidades,
        'desempenho_escolar': desempenho
    }

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