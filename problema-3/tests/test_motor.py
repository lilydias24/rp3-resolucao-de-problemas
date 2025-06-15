import unittest
from unittest.mock import patch
from logic import MotorDeInferencia

# Simulação de regra vinda do banco
mock_regras = [
    {
        'carreira': 'Desenvolvedor(a)',
        'justificativa': 'Alta afinidade com programação',
        'interesses': ['programação', 'tecnologia'],
        'habilidades': ['Python', 'resolução de problemas'],
        'desempenho': {
            'matemática': {'nota_min': 7.0, 'peso': 1},
            'lógica': {'nota_min': 6.0, 'peso': 1}
        }
    },
    {
        'carreira': 'Engenheiro(a) de Dados',
        'justificativa': 'Combinação de estatística e programação',
        'interesses': ['dados', 'programação'],
        'habilidades': ['SQL', 'Python'],
        'desempenho': {
            'matemática': {'nota_min': 8.0, 'peso': 2}
        }
    }
]

# Simulação de perfil do estudante
mock_estudante = {
    'interesses': ['programação', 'tecnologia'],
    'habilidades': ['Python', 'resolução de problemas'],
    'desempenho_escolar': {
        'matemática': 8.5,
        'lógica': 7.0
    }
}

class TestMotorDeInferencia(unittest.TestCase):

    @patch.object(MotorDeInferencia, '_buscar_regras_do_banco', return_value=mock_regras)
    def test_processa_estudante_recomendado(self, mock_busca):
        motor = MotorDeInferencia()
        recomendadas, proximas = motor.processa_estudante(mock_estudante)

        self.assertEqual(len(recomendadas), 1)
        self.assertEqual(recomendadas[0]['carreira'], 'Desenvolvedor(a)')
        self.assertGreater(recomendadas[0]['score'], 90)
        self.assertIsInstance(recomendadas[0]['explicacao'], dict)
        self.assertEqual(len(proximas), 1)
        self.assertEqual(proximas[0]['carreira'], 'Engenheiro(a) de Dados')

    @patch.object(MotorDeInferencia, '_buscar_regras_do_banco', return_value=mock_regras)
    def test_processa_estudante_nenhum_totalmente_atendido(self, mock_busca):
        estudante_incompleto = {
            'interesses': ['literatura'],
            'habilidades': ['desenho'],
            'desempenho_escolar': {'história': 5.0}
        }
        motor = MotorDeInferencia()
        recomendadas, proximas = motor.processa_estudante(estudante_incompleto)

        self.assertEqual(len(recomendadas), 0)
        self.assertTrue(all('carreira' in p for p in proximas))

    @patch.object(MotorDeInferencia, '_buscar_regras_do_banco', return_value=[])
    def test_processa_estudante_sem_regras(self, mock_busca):
        motor = MotorDeInferencia()
        recomendadas, proximas = motor.processa_estudante(mock_estudante)

        self.assertEqual(recomendadas, [])
        self.assertEqual(proximas, [])

if __name__ == "__main__":
    unittest.main()
