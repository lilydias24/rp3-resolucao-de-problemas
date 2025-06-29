import unittest
from unittest.mock import patch, MagicMock

from logic import MotorDeInferencia

class TestMotorDeInferencia(unittest.TestCase):
    @patch('motor_inferencia.conectar')
    def test_buscar_regras_do_banco(self, mock_conectar):
        # Setup mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Define fake fetchall responses in sequence:
        # 1) regras_carreira
        # 2) interesses
        # 3) habilidades
        # 4) desempenho
        mock_cursor.fetchall.side_effect = [
            [(1, 'Engenheiro', 'Justificativa')],           # regras_carreira
            [('interesse1',), ('interesse2',)],             # interesses
            [('habilidade1',)],                              # habilidades
            [('matematica', 7.0, 2)],                        # desempenho
        ]

        mi = MotorDeInferencia()
        resultado = mi._buscar_regras_do_banco()

        expected = [{
            'carreira': 'Engenheiro',
            'justificativa': 'Justificativa',
            'interesses': ['interesse1', 'interesse2'],
            'habilidades': ['habilidade1'],
            'desempenho': {'matematica': {'nota_min': 7.0, 'peso': 2}}
        }]
        self.assertEqual(resultado, expected)
        mock_conn.close.assert_called_once()

    @patch.object(MotorDeInferencia, '_buscar_regras_do_banco')
    def test_processa_estudante_recomendadas(self, mock_buscar):
        # Setup one rule that is fully satisfied by the student
        regras = [{
            'carreira': 'Analista de Dados',
            'justificativa': 'Just because',
            'interesses': ['analise', 'programacao'],
            'habilidades': ['python', 'estatistica'],
            'desempenho': {'matematica': {'nota_min': 8.0, 'peso': 1}}
        }]
        mock_buscar.return_value = regras

        estudante = {
            'interesses': ['analise', 'programacao'],
            'habilidades': ['python', 'estatistica'],
            'desempenho_escolar': {'matematica': 9.0}
        }

        mi = MotorDeInferencia()
        recomendadas, proximas = mi.processa_estudante(estudante)

        self.assertEqual(len(recomendadas), 1)
        self.assertEqual(recomendadas[0]['carreira'], 'Analista de Dados')
        self.assertEqual(proximas, [])

    @patch.object(MotorDeInferencia, '_buscar_regras_do_banco')
    def test_processa_estudante_proximas(self, mock_buscar):
        # Setup one rule that is not fully satisfied
        regras = [{
            'carreira': 'Desenvolvedor',
            'justificativa': 'Dev needed',
            'interesses': ['coding', 'design'],
            'habilidades': ['java'],
            'desempenho': {'logica': {'nota_min': 6.0, 'peso': 1}}
        }]
        mock_buscar.return_value = regras

        estudante = {
            'interesses': ['coding'],
            'habilidades': [],
            'desempenho_escolar': {'logica': 5.0}
        }

        mi = MotorDeInferencia()
        recomendadas, proximas = mi.processa_estudante(estudante)

        self.assertEqual(recomendadas, [])
        self.assertEqual(len(proximas), 1)
        self.assertEqual(proximas[0]['carreira'], 'Desenvolvedor')
        # Score should be ((1/2 + 0/1 + 0/1)/3)*100 = 16.67
        expected_score = round(((1/2 + 0 + 0) / 3) * 100, 2)
        self.assertAlmostEqual(proximas[0]['score'], expected_score)

if __name__ == '__main__':
    unittest.main()
