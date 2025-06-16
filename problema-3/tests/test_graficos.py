import os
import tempfile
import unittest
from graficos import GeradorGraficos
from unittest.mock import patch

class TestSanitizarNome(unittest.TestCase):
    def setUp(self):
        # Use a temporary directory to avoid cluttering the file system
        self.gg = GeradorGraficos(diretorio_saida=tempfile.mkdtemp())

    def test_sanitizar_nome_removes_special_chars_and_lowercases(self):
        nome = "Matemática Avançada!"
        # 'á' and ' ' and '!' should be replaced by '_', and all letters lowercased
        expected = "matem_tica_avan_ada_"
        result = self.gg._sanitizar_nome(nome)
        self.assertEqual(result, expected)

class TestGraficoDesempenhoDisciplina(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.gg = GeradorGraficos(diretorio_saida=self.tempdir)

    def test_empty_data_prints_message(self):
        with patch('builtins.print') as mock_print:
            self.gg.grafico_desempenho_disciplina([], "Disciplina")
            mock_print.assert_called_with("Nenhum dado fornecido para gerar o gráfico de disciplina.")

    def test_missing_columns_prints_message(self):
        dados = [{'foo': 1, 'bar': 2}]
        with patch('builtins.print') as mock_print:
            self.gg.grafico_desempenho_disciplina(dados, "Disciplina")
            mock_print.assert_called_with("Colunas esperadas ('estudante' e 'nota') ausentes.")

    def test_success_creates_file(self):
        dados = [
            {'estudante': 'Alice', 'nota': 9},
            {'estudante': 'Bob', 'nota': 7}
        ]
        disciplina = "Matemática"
        self.gg.grafico_desempenho_disciplina(dados, disciplina)
        nome_arquivo = f"desempenho_{self.gg._sanitizar_nome(disciplina)}.png"
        caminho = os.path.join(self.tempdir, nome_arquivo)
        self.assertTrue(os.path.exists(caminho))

class TestGraficoDesempenhoEstudante(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.gg = GeradorGraficos(diretorio_saida=self.tempdir)

    def test_empty_data_prints_message(self):
        with patch('builtins.print') as mock_print:
            self.gg.grafico_desempenho_estudante([], "Estudante")
            mock_print.assert_called_with("Nenhum dado fornecido para gerar o gráfico do estudante.")

    def test_missing_columns_prints_message(self):
        dados = [{'foo': 1, 'bar': 2}]
        with patch('builtins.print') as mock_print:
            self.gg.grafico_desempenho_estudante(dados, "Estudante")
            mock_print.assert_called_with("Colunas esperadas ('disciplina' e 'nota') ausentes.")

    def test_success_creates_file(self):
        dados = [
            {'disciplina': 'Portugues', 'nota': 8},
            {'disciplina': 'Historia', 'nota': 6}
        ]
        estudante = "Maria"
        self.gg.grafico_desempenho_estudante(dados, estudante)
        nome_arquivo = f"desempenho_{self.gg._sanitizar_nome(estudante)}.png"
        caminho = os.path.join(self.tempdir, nome_arquivo)
        self.assertTrue(os.path.exists(caminho))

class TestGraficoRecomendacoes(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.gg = GeradorGraficos(diretorio_saida=self.tempdir)

    def test_empty_data_prints_message(self):
        with patch('builtins.print') as mock_print:
            self.gg.grafico_recomendacoes([])
            mock_print.assert_called_with("Nenhum dado fornecido para gerar o gráfico de recomendações.")

    def test_missing_column_prints_message(self):
        dados = [{'foo': 'Dev'}]
        with patch('builtins.print') as mock_print:
            self.gg.grafico_recomendacoes(dados)
            mock_print.assert_called_with("Coluna esperada ('carreira') ausente.")

    def test_success_creates_file(self):
        dados = [
            {'carreira': 'Dev'},
            {'carreira': 'Data'},
            {'carreira': 'Dev'}
        ]
        self.gg.grafico_recomendacoes(dados)
        caminho = os.path.join(self.tempdir, 'distribuicao_recomendacoes.png')
        self.assertTrue(os.path.exists(caminho))

if __name__ == '__main__':
    unittest.main()
