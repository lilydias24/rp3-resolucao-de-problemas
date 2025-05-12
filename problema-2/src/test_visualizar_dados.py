import unittest
from unittest import FunctionTestCase
from visualizar_dados import transformar_linha_para_dict,limitar_observacoes


def test_transformar_linha_para_dict_h():
    head = "x,y,z"
    linha = "1,2,3"
    saida = {"x":"1","y":"2","z":"3"}
    assert transformar_linha_para_dict(head,linha) == saida

def test_transformar_linha_para_dict_s():
    head = "x,y,z,a,b,c,d"
    linha = "1,2,3"
    try:
        transformar_linha_para_dict(head,linha)
        assert False, "not value error"
    except ValueError:
        assert "numero de dados incorreto"

def test_limitar_observacoes_h():
    registro = {"obs":"a"*99}
    assert limitar_observacoes(registro) == registro

def test_limitar_observacoes_s():
    registro = {"obs": "a"*20000}
    limite = limitar_observacoes(registro)
    assert len(limite["obs"]) > 101





if __name__ == '__main__':

    suite = unittest.TestSuite([
        FunctionTestCase(test_transformar_linha_para_dict_h),
        FunctionTestCase(test_transformar_linha_para_dict_s),
        FunctionTestCase(test_limitar_observacoes_h),
        FunctionTestCase(test_limitar_observacoes_s)
    ])
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
