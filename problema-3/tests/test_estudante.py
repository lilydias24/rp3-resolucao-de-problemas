import unittest
from models.estudante import Estudante


class TestEstudante(unittest.TestCase):
    '''
    fixture para teste
    '''

    def setUp(self):
        self.aluno = Estudante("Alice")

    # ----- adicionar_habilidade -----
    def test_adicionar_habilidade(self):
        # teste valor válido
        self.aluno.adicionar_habilidade("Programação")
        self.assertIn("programação", self.aluno.habilidades)

        # teste entrada com espaços
        self.aluno.adicionar_habilidade("  Física  ")
        self.assertIn("física", self.aluno.habilidades)

        # teste valor duplicado
        self.aluno.adicionar_habilidade("matemática")
        tamanho_antes = len(self.aluno.habilidades)
        self.aluno.adicionar_habilidade("matemática")
        self.assertEqual(len(self.aluno.habilidades), tamanho_antes)

        #teste valor inválido
        with self.assertRaises(TypeError):
            self.aluno.adicionar_habilidade(123)

        #teste valor vazio
        with self.assertRaises(ValueError):
            self.aluno.adicionar_habilidade("   ")

    # ----- metricas_escola -----
    def test_metricas_escola_novo_registro(self):
        historico = self.aluno.metricas_escola("Química", 7.5)
        self.assertEqual(len(historico), 1)
        self.assertEqual(historico[0], {"Química": 7.5})

    def test_metricas_escola_atualiza_registro(self):
        self.aluno.metricas_escola("Biologia", 5.0)
        historico = self.aluno.metricas_escola("Biologia", 9.0)
        self.assertEqual(len(historico), 1)
        self.assertEqual(historico[0]["Biologia"], 9.0)

    def test_metricas_escola_insere_nova_materia_em_historico_existente(self):
        self.aluno.metricas_escola("História", 6.0)
        historico = self.aluno.metricas_escola("Geografia", 8.0)
        self.assertEqual(len(historico), 2)

        # verifica que ambas matérias estão no histórico
        materias = {list(reg)[0] for reg in historico}
        self.assertSetEqual(materias, {"História", "Geografia"})

    def test_metricas_escola_tipo_materia_invalido(self):
        with self.assertRaises(TypeError):
            self.aluno.metricas_escola(456, 7.0)

    def test_metricas_escola_materia_vazia(self):
        with self.assertRaises(ValueError):
            self.aluno.metricas_escola("   ", 7.0)

    def test_metricas_escola_desempenho_tipo_invalido(self):
        with self.assertRaises(TypeError):
            self.aluno.metricas_escola("Arte", "nota")

    # ----- possiveis_carreiras -----
    def test_possiveis_carreiras_sem_habilidades(self):
        self.assertEqual(self.aluno.possiveis_carreiras(), ["carreira não definida"])

    def test_possiveis_carreiras_com_habilidades_conhecidas(self):
        self.aluno.adicionar_habilidade("programação")
        self.aluno.adicionar_habilidade("física")
        carreiras = self.aluno.possiveis_carreiras()
        self.assertListEqual(
            carreiras,
            ["Desenvolvedor(a)", "Engenheiro(a) de Hardware"]
        )

    def test_possiveis_carreiras_habilidade_nao_mapeada(self):
        self.aluno.adicionar_habilidade("culinária")
        self.assertEqual(self.aluno.possiveis_carreiras(), ["carreira não definida"])


if __name__ == "__main__":
    unittest.main()
