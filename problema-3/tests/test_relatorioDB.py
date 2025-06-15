import unittest
from unittest.mock import patch
from .data import RelatorioDB

# Dados simulados
mock_estudantes = [
    (1, "Alice", ["programação"], {"programação", "matemática"}, {"matemática": 9.5, "física": 8}),
    (2, "Bruno", ["física"], {"física"}, {"física": 7.0}),
    (3, "Carla", [], {"química"}, {}),
]

class TestRelatorioDB(unittest.TestCase):

    @patch("relatorio.listar_estudantes", return_value=mock_estudantes)
    def test_listar_estudantes(self, mock_listar):
        rel = RelatorioDB()
        estudantes = rel.listar_estudantes()
        self.assertIsInstance(estudantes, list)
        self.assertEqual(len(estudantes), 3)
        self.assertEqual(estudantes[0][1], "Alice")

    @patch("relatorio.listar_estudantes", return_value=mock_estudantes)
    def test_obter_disciplinas(self, mock_listar):
        rel = RelatorioDB()
        disciplinas = rel.obter_disciplinas()
        self.assertIn("matemática", disciplinas)
        self.assertIn("física", disciplinas)
        self.assertNotIn("química", disciplinas)  # Carla não tem desempenho

    @patch("relatorio.listar_estudantes", return_value=mock_estudantes)
    def test_obter_desempenho_disciplina(self, mock_listar):
        rel = RelatorioDB()
        desempenho = rel.obter_desempenho_disciplina("física")
        self.assertEqual(len(desempenho), 2)
        for d in desempenho:
            self.assertIn("estudante", d)
            self.assertIn("nota", d)

    @patch("relatorio.listar_estudantes", return_value=mock_estudantes)
    def test_obter_desempenho_estudante(self, mock_listar):
        rel = RelatorioDB()
        desempenho = rel.obter_desempenho_estudante("Alice")
        disciplinas = [d["disciplina"] for d in desempenho]
        self.assertIn("matemática", disciplinas)
        self.assertIn("física", disciplinas)

    @patch("relatorio.listar_estudantes", return_value=mock_estudantes)
    def test_obter_recomendacoes(self, mock_listar):
        rel = RelatorioDB()
        recomendacoes = rel.obter_recomendacoes()
        self.assertIn({'estudante': 'Alice', 'carreira': 'programação'}, recomendacoes)
        self.assertIn({'estudante': 'Bruno', 'carreira': 'física'}, recomendacoes)
        self.assertNotIn({'estudante': 'Carla', 'carreira': 'química'}, recomendacoes)

if __name__ == "__main__":
    unittest.main()
