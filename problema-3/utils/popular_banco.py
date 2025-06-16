from logic.estudante import salvar_estudante

def popular_banco():
    """
    Popula o banco de dados com dados de exemplo.
    """
    # Dados de exemplo
    estudantes = [
        {
            'nome': 'Ana',
            'interesses': ['programação', 'matemática', 'lógica'],
            'habilidades': ['resolução de problemas', 'análise de dados', 'programação'],
            'desempenho_escolar': {
                'Matemática': 9.5,
                'Física': 8.5,
                'Química': 7.5,
                'Português': 8.0,
                'História': 7.0,
                'Geografia': 7.5,
                'Inglês': 8.5,
                'Biologia': 7.0
            }
        },
        {
            'nome': 'Bruno',
            'interesses': ['design', 'arte', 'criatividade'],
            'habilidades': ['design gráfico', 'ilustração', 'comunicação visual'],
            'desempenho_escolar': {
                'Matemática': 7.0,
                'Física': 6.5,
                'Química': 6.0,
                'Português': 8.5,
                'História': 8.0,
                'Geografia': 7.5,
                'Inglês': 8.0,
                'Biologia': 6.5
            }
        },
        {
            'nome': 'Carla',
            'interesses': ['medicina', 'biologia', 'saúde'],
            'habilidades': ['análise', 'observação', 'comunicação'],
            'desempenho_escolar': {
                'Matemática': 8.0,
                'Física': 7.5,
                'Química': 9.0,
                'Português': 8.5,
                'História': 7.0,
                'Geografia': 7.0,
                'Inglês': 8.0,
                'Biologia': 9.5
            }
        },
        {
            'nome': 'Diego',
            'interesses': ['engenharia', 'física', 'matemática'],
            'habilidades': ['cálculo', 'resolução de problemas', 'análise'],
            'desempenho_escolar': {
                'Matemática': 9.0,
                'Física': 9.5,
                'Química': 8.5,
                'Português': 7.5,
                'História': 6.5,
                'Geografia': 7.0,
                'Inglês': 7.5,
                'Biologia': 7.0
            }
        },
        {
            'nome': 'Eduarda',
            'interesses': ['direito', 'história', 'comunicação'],
            'habilidades': ['argumentação', 'pesquisa', 'escrita'],
            'desempenho_escolar': {
                'Matemática': 7.0,
                'Física': 6.5,
                'Química': 6.0,
                'Português': 9.5,
                'História': 9.0,
                'Geografia': 8.5,
                'Inglês': 8.0,
                'Biologia': 7.0
            }
        },
        {
            'nome': 'Felipe',
            'interesses': ['marketing', 'comunicação', 'negócios'],
            'habilidades': ['criatividade', 'persuasão', 'análise de mercado'],
            'desempenho_escolar': {
                'Matemática': 7.5,
                'Física': 6.5,
                'Química': 6.0,
                'Português': 8.5,
                'História': 8.0,
                'Geografia': 8.5,
                'Inglês': 8.5,
                'Biologia': 6.5
            }
        },
        {
            'nome': 'Giovana',
            'interesses': ['psicologia', 'comportamento', 'comunicação'],
            'habilidades': ['empatia', 'escuta ativa', 'análise'],
            'desempenho_escolar': {
                'Matemática': 7.0,
                'Física': 6.0,
                'Química': 6.5,
                'Português': 9.0,
                'História': 8.5,
                'Geografia': 8.0,
                'Inglês': 8.5,
                'Biologia': 8.0
            }
        },
        {
            'nome': 'Henrique',
            'interesses': ['administração', 'negócios', 'economia'],
            'habilidades': ['liderança', 'planejamento', 'análise financeira'],
            'desempenho_escolar': {
                'Matemática': 8.5,
                'Física': 7.0,
                'Química': 6.5,
                'Português': 8.0,
                'História': 8.0,
                'Geografia': 8.5,
                'Inglês': 8.0,
                'Biologia': 6.5
            }
        },
        {
            'nome': 'Isabela',
            'interesses': ['arquitetura', 'design', 'arte'],
            'habilidades': ['criatividade', 'desenho', 'planejamento'],
            'desempenho_escolar': {
                'Matemática': 8.0,
                'Física': 7.5,
                'Química': 6.5,
                'Português': 8.5,
                'História': 8.0,
                'Geografia': 8.5,
                'Inglês': 8.0,
                'Biologia': 7.0
            }
        },
        {
            'nome': 'João',
            'interesses': ['ciência da computação', 'programação', 'matemática'],
            'habilidades': ['lógica', 'resolução de problemas', 'programação'],
            'desempenho_escolar': {
                'Matemática': 9.0,
                'Física': 8.5,
                'Química': 7.0,
                'Português': 7.5,
                'História': 6.5,
                'Geografia': 7.0,
                'Inglês': 7.5,
                'Biologia': 6.5
            }
        }
    ]

    # Cadastra cada estudante
    for estudante in estudantes:
        try:
            salvar_estudante(estudante)
        except Exception as e:
            pass  # Ignora erros de duplicação