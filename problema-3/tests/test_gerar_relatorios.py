import unittest
from unittest.mock import patch, MagicMock
from gerar_relatorios import gerar_relatorios, obter_estudantes_silencioso
"""
test_gerar_relatorios.py
Testes para o módulo gerar_relatorios:
- obter_estudantes_silencioso(): sucesso e falha de conexão
- gerar_relatorios(): integração com RelatorioDB e GeradorGraficos sem exceções
"""
class TestGerarRelatorios(unittest.TestCase):

    @patch("gerar_relatorios.conectar")
    def test_obter_estudantes_silencioso_sucesso(self, mock_conectar):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (1, "Alice", '["programação"]', '["python"]', '{"matemática": 8.5}')
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_conectar.return_value = mock_conn

        estudantes = obter_estudantes_silencioso()
        self.assertEqual(len(estudantes), 1)
        self.assertEqual(estudantes[0][1], "Alice")
        self.assertEqual(estudantes[0][2], ["programação"])
        self.assertEqual(estudantes[0][4], {"matemática": 8.5})

    @patch("gerar_relatorios.GeradorGraficos")
    @patch("gerar_relatorios.RelatorioDB")
    @patch("gerar_relatorios.obter_estudantes_silencioso")
    def test_gerar_relatorios_com_dados(self, mock_obter_estudantes, mock_db_cls, mock_graficos_cls):
        mock_obter_estudantes.return_value = [
            (1, "João", ["matemática"], ["lógica"], {"matemática": 9.0})
        ]

        mock_db = MagicMock()
        mock_db.obter_disciplinas.return_value = ["matemática"]
        mock_db.obter_desempenho_disciplina.return_value = {"João": 9.0}
        mock_db.obter_desempenho_estudante.return_value = {"matemática": 9.0}
        mock_db.obter_recomendacoes.return_value = {"Analista de Dados": 1}

        mock_db_cls.return_value = mock_db
        mock_graficos_cls.return_value = MagicMock()

        try:
            gerar_relatorios()  # Não deve lançar exceção
        except Exception:
            self.fail("gerar_relatorios() lançou uma exceção inesperada.")

    @patch("gerar_relatorios.conectar", side_effect=Exception("Erro de conexão"))
    def test_obter_estudantes_silencioso_erro(self, _):
        from data import ConexaoErro
        with self.assertRaises(ConexaoErro):
            obter_estudantes_silencioso()

if __name__ == "__main__":
    unittest.main()
