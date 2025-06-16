import unittest
from motor import MotorDeInferencia
from unittest.mock import patch

class FakeCursor:
    def __init__(self):
        self.last_sql = None

    def execute(self, sql, params=None):
        self.last_sql = sql.strip()

    def fetchall(self):
        # Simula retornos diferentes conforme a consulta
        if self.last_sql.startswith("SELECT id, carreira"):
            # Regra de carreira
            return [(1, 'CarreiraTeste', 'JustificativaTeste')]
        elif "FROM interesses_regra" in self.last_sql:
            return [('interesse1',), ('interesse2',)]
        elif "FROM habilidades_regra" in self.last_sql:
            return [('habilidade1',)]
        elif "FROM desempenho_regra" in self.last_sql:
            return [("Matematica", 7.0, 0.5), ("Fisica", 8.0, 0.5)]
        return []

class FakeConn:
    def __init__(self):
        self._cursor = FakeCursor()

    def cursor(self):
        return self._cursor

    def close(self):
        pass

class TestMotorDeInferencia(unittest.TestCase):
    @patch('motor.conectar', return_value=FakeConn())
    def test_buscar_regras_do_banco(self, mock_conectar):
        md = MotorDeInferencia()
        regras = md._buscar_regras_do_banco()
        self.assertEqual(len(regras), 1)
        regra = regras[0]
        self.assertEqual(regra['carreira'], 'CarreiraTeste')
        self.assertEqual(regra['justificativa'], 'JustificativaTeste')
        self.assertListEqual(regra['interesses'], ['interesse1', 'interesse2'])
        self.assertListEqual(regra['habilidades'], ['habilidade1'])
        self.assertDictEqual(
            regra['desempenho'],
            {'Matematica': {'nota_min': 7.0, 'peso': 0.5}, 'Fisica': {'nota_min': 8.0, 'peso': 0.5}}
        )

    @patch('motor.conectar', return_value=FakeConn())
    def test_processa_estudante_completo(self, mock_conectar):
        md = MotorDeInferencia()
        estudante = {
            'interesses': ['interesse1', 'interesse2'],
            'habilidades': ['habilidade1'],
            'desempenho_escolar': {'Matematica': 7.0, 'Fisica': 8.0}
        }
        recomendadas, proximas = md.processa_estudante(estudante)
        self.assertEqual(len(recomendadas), 1)
        self.assertEqual(len(proximas), 0)
        rec = recomendadas[0]
        self.assertEqual(rec['carreira'], 'CarreiraTeste')
        self.assertAlmostEqual(rec['score'], 100.0)
        self.assertIn('Interesse', rec['explicacao'])
        self.assertIn('Habilidade', rec['explicacao'])
        self.assertIn('Desempenho', rec['explicacao'])

    @patch('motor.conectar', return_value=FakeConn())
    def test_processa_estudante_incompleto(self, mock_conectar):
        md = MotorDeInferencia()
        estudante = {
            'interesses': ['interesse1'],
            'habilidades': [],
            'desempenho_escolar': {'Matematica': 6.0}
        }
        recomendadas, proximas = md.processa_estudante(estudante)
        self.assertEqual(len(recomendadas), 0)
        self.assertEqual(len(proximas), 1)
        prox = proximas[0]
        self.assertEqual(prox['carreira'], 'CarreiraTeste')
        self.assertTrue(prox['score'] < 100.0)
        self.assertIn('Faltam', prox['explicacao']['Interesse'])
        self.assertIn('Faltam', prox['explicacao']['Habilidade'])
        self.assertIn('Faltam', prox['explicacao']['Desempenho'])

if __name__ == '__main__':
    unittest.main()
