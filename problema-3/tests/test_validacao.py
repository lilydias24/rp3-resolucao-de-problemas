import unittest
from data.validacao import *


class TestValidacao(unittest.TestCase):

    # --- sanitizar_nome ---
    def test_sanitizar_nome_valido(self):
        self.assertEqual(sanitizar_nome(" João Silva "), "João Silva")

    def test_sanitizar_nome_invalido_curto(self):
        with self.assertRaises(ValidacaoErro):
            sanitizar_nome("Jo")

    def test_sanitizar_nome_invalido_vazio(self):
        with self.assertRaises(ValidacaoErro):
            sanitizar_nome("")

    def test_sanitizar_tipo_invalido(self):
        with self.assertRaises(ValidacaoErro):
            sanitizar_nome(123)

    def test_sanitizar_caracteres_especiais(self):
        self.assertEqual(sanitizar_nome("Ana!@# dos Santos"), "Ana dos Santos")

    # --- validar_interesses ---
    def test_validar_interesses_validos(self):
        self.assertEqual(validar_interesses(["Programação", "  Física  "]), ["Programação", "Física"])

    def test_validar_interesses_vazio(self):
        with self.assertRaises(ValidacaoErro):
            validar_interesses([])

    def test_validar_interesses_invalidos(self):
        with self.assertRaises(ValidacaoErro):
            validar_interesses("não é lista")

    # --- validar_habilidades ---
    def test_validar_habilidades_validas(self):
        self.assertEqual(validar_habilidades(["Python", " Matemática "]), ["Python", "Matemática"])

    def test_validar_habilidades_vazia(self):
        with self.assertRaises(ValidacaoErro):
            validar_habilidades([])

    def test_validar_habilidades_invalida(self):
        with self.assertRaises(ValidacaoErro):
            validar_habilidades("não é lista")

    # --- validar_desempenho ---
    def test_validar_desempenho_valido(self):
        dados = {"matemática": 8.5, "física": 9}
        self.assertEqual(validar_desempenho(dados), dados)

    def test_validar_desempenho_limites(self):
        dados = {"química": 0, "biologia": 10}
        self.assertEqual(validar_desempenho(dados), dados)

    def test_validar_desempenho_nota_invalida(self):
        with self.assertRaises(ValidacaoErro):
            validar_desempenho({"física": 11})

    def test_validar_desempenho_entrada_invalida(self):
        with self.assertRaises(ValidacaoErro):
            validar_desempenho("isso não é um dicionário")

    # --- validar_estudante ---
    def test_validar_estudante_completo_valido(self):
        estudante = {
            "nome": "Maria Clara",
            "interesses": ["Programação"],
            "habilidades": ["Python"],
            "desempenho_escolar": {"matemática": 9.0}
        }
        resultado = validar_estudante(estudante)
        self.assertEqual(resultado[0], "Maria Clara")
        self.assertIn("Programação", resultado[1])
        self.assertIn("Python", resultado[2])
        self.assertEqual(resultado[3], {"matemática": 9.0})

    def test_validar_estudante_invalido(self):
        estudante = {
            "nome": "MC",
            "interesses": [],
            "habilidades": ["ok"],
            "desempenho_escolar": {}
        }
        with self.assertRaises(ValidacaoErro):
            validar_estudante(estudante)


if __name__ == "__main__":
    unittest.main()
