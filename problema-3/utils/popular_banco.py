from logic.estudante import salvar_estudante

def popular_banco_com_estudantes():
    """
    Popula o banco de dados com 10 estudantes fictícios para testes.
    Os interesses, habilidades e disciplinas devem já existir no banco.
    """
    exemplos = [
        {
            'nome': 'Ana',
            'interesses': ['Matemática', 'Tecnologia'],
            'habilidades': ['Lógica', 'Programação'],
            'desempenho_escolar': {'Matemática': 9.5, 'Português': 8.0, 'Física': 8.5}
        },
        {
            'nome': 'Bruno',
            'interesses': ['Biologia', 'Saúde'],
            'habilidades': ['Empatia', 'Comunicação'],
            'desempenho_escolar': {'Biologia': 9.0, 'Química': 7.5, 'Matemática': 6.0}
        },
        {
            'nome': 'Carla',
            'interesses': ['Artes', 'Comunicação'],
            'habilidades': ['Criatividade', 'Desenho'],
            'desempenho_escolar': {'Artes': 10.0, 'Português': 8.5, 'História': 7.0}
        },
        {
            'nome': 'Diego',
            'interesses': ['Tecnologia', 'Engenharia'],
            'habilidades': ['Programação', 'Resolução de Problemas'],
            'desempenho_escolar': {'Matemática': 8.0, 'Física': 8.5, 'Química': 7.5}
        },
        {
            'nome': 'Eduarda',
            'interesses': ['Saúde', 'Química'],
            'habilidades': ['Empatia', 'Trabalho em Equipe'],
            'desempenho_escolar': {'Biologia': 8.5, 'Química': 9.0, 'Matemática': 7.0}
        },
        {
            'nome': 'Felipe',
            'interesses': ['História', 'Política'],
            'habilidades': ['Comunicação', 'Análise Crítica'],
            'desempenho_escolar': {'História': 9.0, 'Geografia': 8.0, 'Português': 7.5}
        },
        {
            'nome': 'Giovana',
            'interesses': ['Matemática', 'Engenharia'],
            'habilidades': ['Lógica', 'Resolução de Problemas'],
            'desempenho_escolar': {'Matemática': 9.0, 'Física': 9.5, 'Química': 8.0}
        },
        {
            'nome': 'Henrique',
            'interesses': ['Tecnologia', 'Jogos'],
            'habilidades': ['Programação', 'Criatividade'],
            'desempenho_escolar': {'Matemática': 8.5, 'Artes': 7.5, 'Física': 7.0}
        },
        {
            'nome': 'Isabela',
            'interesses': ['Comunicação', 'Artes'],
            'habilidades': ['Desenho', 'Comunicação'],
            'desempenho_escolar': {'Artes': 9.5, 'Português': 8.0, 'História': 8.5}
        },
        {
            'nome': 'João',
            'interesses': ['Política', 'História'],
            'habilidades': ['Análise Crítica', 'Comunicação'],
            'desempenho_escolar': {'História': 8.5, 'Geografia': 8.0, 'Matemática': 6.5}
        }
    ]

    for estudante in exemplos:
        try:
            salvar_estudante(estudante)
            print(f"Estudante {estudante['nome']} cadastrado.")
        except Exception as e:
            print(f"Erro ao cadastrar {estudante['nome']}: {e}")

# Para rodar, basta chamar:
popular_banco_com_estudantes()