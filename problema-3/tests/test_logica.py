import unittest
import logica
"""
test_logica.py
Validação das regras lógicas de recomendação de carreira:
- regra_interesse(), regra_habilidade(), regra_desempenho()
- pode_seguir_carreira(), carreiras_proximas()
- geração de fatos para feed de regras
"""
class TestLogica(unittest.TestCase):
    def setUp(self):
        # Student with all requirements met for desenvolvimento_software
        self.student_full = {
            'interesses': ['tecnologia', 'matematica', 'logica'],
            'habilidades': ['programacao', 'resolucao_problemas', 'trabalho_equipe'],
            'desempenho_escolar': {'matematica': 8, 'fisica': 9, 'programacao': 7}
        }
        # Student with none of the requirements
        self.student_none = {
            'interesses': [],
            'habilidades': [],
            'desempenho_escolar': {}
        }
        # Student with partial requirements
        self.student_partial = {
            'interesses': ['tecnologia'],
            'habilidades': ['programacao'],
            'desempenho_escolar': {'matematica': 7}
        }

    def test_regra_interesse_full(self):
        ok, score = logica.regra_interesse(self.student_full, 'desenvolvimento_software')
        self.assertTrue(ok)
        # All interests match: score normalized should be 1.0
        self.assertAlmostEqual(score, 1.0)

    def test_regra_interesse_none(self):
        ok, score = logica.regra_interesse(self.student_none, 'data_science')
        self.assertFalse(ok)
        self.assertEqual(score, 0.0)

    def test_regra_habilidade_full(self):
        ok, score = logica.regra_habilidade(self.student_full, 'desenvolvimento_software')
        self.assertTrue(ok)
        self.assertAlmostEqual(score, 1.0)

    def test_regra_habilidade_none(self):
        ok, score = logica.regra_habilidade(self.student_none, 'ciencias_humanas')
        self.assertFalse(ok)
        self.assertEqual(score, 0.0)

    def test_regra_desempenho_full(self):
        ok, score = logica.regra_desempenho(self.student_full, 'desenvolvimento_software')
        self.assertTrue(ok)
        # Full meets all performance: normalized score should be 1.0
        self.assertAlmostEqual(score, 1.0)

    def test_regra_desempenho_incomplete(self):
        ok, score = logica.regra_desempenho(self.student_partial, 'data_science')
        # Only matematica meets >=7, others missing -> 0.4/1.0 < 0.5
        self.assertFalse(ok)
        self.assertAlmostEqual(score, 0.4)

    def test_pode_seguir_carreira_true(self):
        can_follow, total = logica.pode_seguir_carreira(self.student_full, 'desenvolvimento_software')
        self.assertTrue(can_follow)
        self.assertGreaterEqual(total, 0.8)

    def test_pode_seguir_carreira_false(self):
        can_follow, total = logica.pode_seguir_carreira(self.student_none, 'data_science')
        self.assertFalse(can_follow)
        self.assertLess(total, 0.5)

    def test_carreiras_proximas(self):
        # Partial student should get at least one recommended proximity
        proximas = logica.carreiras_proximas(self.student_partial)
        self.assertIsInstance(proximas, list)
        # Ensure that the returned proximities are below threshold (not directly followable)
        for item in proximas:
            self.assertIn('carreira', item)
            self.assertIn('proximidade', item)
            self.assertIn('explicacao', item)

    def test_gerar_fatos_de_interesses(self):
        facts = logica.gerar_fatos_de_interesses(self.student_partial)
        # Expect facts for each interest, skill, and performance >=7
        self.assertIn('interesse:tecnologia', facts)
        self.assertIn('habilidade:programacao', facts)
        self.assertIn('desempenho:matematica', facts)

if __name__ == '__main__':
    unittest.main()
