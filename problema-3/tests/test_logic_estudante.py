import unittest
from unittest.mock import patch
import io
import sys
import sqlite3
import estudante
"""
test_logic_estudante.py
Testes de funções utilitárias do módulo estudante.py (paradigma lógico):
- exibir_estudantes(): exibição formatada ou aviso de lista vazia
- coletar_opcoes(): parsing de input do usuário
- listar_estudantes() e buscar_estudante_completo_por_nome(): integração com SQLite
- recomendar_carreiras(): retorno e persistência de recomendações
"""
class TestExibirEstudantes(unittest.TestCase):
    def test_empty(self):
        captured = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured
        try:
            estudante.exibir_estudantes([])
        finally:
            sys.stdout = original_stdout
        output = captured.getvalue()
        self.assertIn("Nenhum estudante cadastrado.", output)

    def test_non_empty(self):
        data = [(1, 'Alice'), (2, 'Bob')]
        captured = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured
        try:
            estudante.exibir_estudantes(data)
        finally:
            sys.stdout = original_stdout
        output = captured.getvalue()
        self.assertIn("=== Estudantes Cadastrados ===", output)
        self.assertIn("ID: 1 | Nome: Alice", output)
        self.assertIn("ID: 2 | Nome: Bob", output)

class TestColetarOpcoes(unittest.TestCase):
    def test_empty_list(self):
        result = estudante.coletar_opcoes([], "titulo")
        self.assertEqual(result, [])

    def test_valid_selection(self):
        with patch('builtins.input', return_value='1,3'):
            result = estudante.coletar_opcoes(['a', 'b', 'c'], "titulo")
            self.assertEqual(result, ['a', 'c'])

    def test_invalid_then_valid(self):
        inputs = ['x', '2']
        with patch('builtins.input', side_effect=inputs):
            result = estudante.coletar_opcoes(['a', 'b', 'c'], "titulo")
            self.assertEqual(result, ['b'])

class TestListarEstudantes(unittest.TestCase):
    @patch('estudante.conectar')
    def test_listar_estudantes(self, mock_conectar):
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE estudantes (id INTEGER PRIMARY KEY, nome TEXT)")
        cursor.execute("INSERT INTO estudantes (nome) VALUES ('Alice')")
        cursor.execute("INSERT INTO estudantes (nome) VALUES ('Bob')")
        conn.commit()
        mock_conectar.return_value = conn

        result = estudante.listar_estudantes()
        self.assertEqual(result, [(1, 'Alice'), (2, 'Bob')])
        conn.close()

class TestBuscarEstudanteCompletoPorNome(unittest.TestCase):
    @patch('estudante.conectar')
    def test_not_found(self, mock_conectar):
        conn = sqlite3.connect(':memory:')
        conn.cursor().execute("CREATE TABLE estudantes (id INTEGER PRIMARY KEY, nome TEXT)")
        conn.commit()
        mock_conectar.return_value = conn

        result = estudante.buscar_estudante_completo_por_nome('Alice')
        self.assertIsNone(result)
        conn.close()

    @patch('estudante.conectar')
    def test_found(self, mock_conectar):
        conn = sqlite3.connect(':memory:')
        c = conn.cursor()
        # Criar tabelas necessárias
        c.execute("CREATE TABLE estudantes (id INTEGER PRIMARY KEY, nome TEXT)")
        c.execute("CREATE TABLE interesses (id INTEGER PRIMARY KEY, interesse TEXT)")
        c.execute("CREATE TABLE interesses_estudante (estudante_id INTEGER, interesse_id INTEGER)")
        c.execute("CREATE TABLE habilidades (id INTEGER PRIMARY KEY, habilidade TEXT)")
        c.execute("CREATE TABLE habilidades_estudante (estudante_id INTEGER, habilidade_id INTEGER)")
        c.execute("CREATE TABLE disciplinas (id INTEGER PRIMARY KEY, disciplina TEXT)")
        c.execute("CREATE TABLE desempenho_estudante (estudante_id INTEGER, disciplina_id INTEGER, nota REAL)")
        # Inserir estudante
        c.execute("INSERT INTO estudantes (nome) VALUES ('Alice')")
        estudante_id = c.lastrowid
        # Inserir interesse
        c.execute("INSERT INTO interesses (interesse) VALUES ('i1')")
        i1_id = c.lastrowid
        c.execute("INSERT INTO interesses_estudante VALUES (?, ?)", (estudante_id, i1_id))
        # Inserir habilidade
        c.execute("INSERT INTO habilidades (habilidade) VALUES ('h1')")
        h1_id = c.lastrowid
        c.execute("INSERT INTO habilidades_estudante VALUES (?, ?)", (estudante_id, h1_id))
        # Inserir disciplina e desempenho
        c.execute("INSERT INTO disciplinas (disciplina) VALUES ('d1')")
        d1_id = c.lastrowid
        c.execute("INSERT INTO desempenho_estudante VALUES (?, ?, ?)", (estudante_id, d1_id, 8.5))
        conn.commit()
        mock_conectar.return_value = conn

        result = estudante.buscar_estudante_completo_por_nome('Alice')
        expected = {
            'nome': 'Alice',
            'interesses': ['i1'],
            'habilidades': ['h1'],
            'desempenho_escolar': {'d1': 8.5}
        }
        self.assertEqual(result, expected)
        conn.close()

class TestRecomendarCarreiras(unittest.TestCase):
    @patch('estudante.salvar_recomendacao')
    def test_recomendar(self, mock_salvar):
        recs = estudante.recomendar_carreiras(
            estudante_id=1,
            interesses=['criatividade'],
            habilidades=['programação'],
            desempenho={}
        )
        # Verifica se retornou as recomendações corretas
        expected = [
            {'carreira': 'Desenvolvedor de Software', 'score': 90},
            {'carreira': 'Designer Gráfico', 'score': 85}
        ]
        self.assertEqual(recs, expected)
        # Verifica chamadas de salvar_recomendacao
        mock_salvar.assert_any_call(1, 'Desenvolvedor de Software', 90)
        mock_salvar.assert_any_call(1, 'Designer Gráfico', 85)

if __name__ == '__main__':
    unittest.main()
