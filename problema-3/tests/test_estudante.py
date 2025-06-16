import unittest
from models.estudante import Estudante
"""
test_estudante.py
Contém casos de teste para a classe Estudante, validando:
- Adição de habilidades (formatos, duplicatas e erros)
- Registro e atualização de métricas escolares
- Geração de possíveis carreiras com base em regras pré-definidas
"""

class TestEstudante(unittest.TestCase):

    def setUp(self):
        self.estudante = Estudante("Mariana")

    def test_adicionar_habilidade_valida(self):
        self.estudante.adicionar_habilidade("Programação")
        self.assertIn("programação", self.estudante.habilidades)

    def test_adicionar_habilidade_com_espacos(self):
        self.estudante.adicionar_habilidade("  Física  ")
        self.assertIn("física", self.estudante.habilidades)

    def test_adicionar_habilidade_duplicada(self):
        self.estudante.adicionar_habilidade("matemática")
        tamanho = len(self.estudante.habilidades)
        self.estudante.adicionar_habilidade("matemática")
        self.assertEqual(len(self.estudante.habilidades), tamanho)

    def test_adicionar_habilidade_tipo_invalido(self):
        with self.assertRaises(TypeError):
            self.estudante.adicionar_habilidade(123)

    def test_adicionar_habilidade_vazia(self):
        with self.assertRaises(ValueError):
            self.estudante.adicionar_habilidade("   ")

    def test_metricas_escola_nova_materia(self):
        resultado = self.estudante.metricas_escola("física", 8.0)
        self.assertIn("física", resultado)
        self.assertEqual(resultado["física"], 8.0)

    def test_metricas_escola_atualiza_materia(self):
        self.estudante.metricas_escola("matemática", 5.0)
        self.estudante.metricas_escola("matemática", 9.0)
        self.assertEqual(self.estudante.desempenho_escolar["matemática"], 9.0)

    def test_metricas_escola_valores_invalidos(self):
        with self.assertRaises(TypeError):
            self.estudante.metricas_escola(10, 8.0)
        with self.assertRaises(ValueError):
            self.estudante.metricas_escola("   ", 8.0)
        with self.assertRaises(TypeError):
            self.estudante.metricas_escola("história", "dez")

    def test_possiveis_carreiras_corretas(self):
        self.estudante.adicionar_habilidade("programação")
        self.estudante.adicionar_habilidade("física")
        carreiras = self.estudante.possiveis_carreiras()
        self.assertIn("Desenvolvedor(a)", carreiras)
        self.assertIn("Engenheiro(a) de Hardware", carreiras)

    def test_possiveis_carreiras_nenhuma(self):
        self.estudante.adicionar_habilidade("culinária")
        carreiras = self.estudante.possiveis_carreiras()
        self.assertEqual(carreiras, ["carreira não definida"])


if __name__ == '__main__':
    unittest.main()
