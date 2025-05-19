from adicionar_exames import recebe_dados,verifica_inteiro,classifica_entrada
import unittest
from unittest.mock import patch
from unittest import TestSuite, FunctionTestCase



'''
teste feliz recebimento dos dados
'''
def test_recebe_dados_h():
    with patch('builtins.input', side_effect=["80", "120", "80", "100"]):
        recebe_func = recebe_dados()
        reg = recebe_func[0]
        assert reg["Batimentos"] == "80"
        assert reg["Pressão Sistólica"] == "120"
        assert reg["Pressão Diastólica"] == "80"
        assert reg["Glicose"] == "100"


'''
testes StopIteration e KeyboardInterrupt
'''
def test_recebe_dados_stop():
    with patch('builtins.input', side_effect=[]):
        try:
            recebe_dados()
            assert False, "não teve stopIteration"
        except StopIteration:
            pass


def test_recebe_dados_keyboard():
    with patch('builtins.input', side_effect=KeyboardInterrupt):
        try:
            recebe_dados()
            assert False, "não teve KeyboardInterrupt"
        except KeyboardInterrupt:
            pass
'''
teste feliz classificação entrada
'''
def test_classifica_entrada_h():
    fake_dados = {
        "Batimentos": "75",
        "Pressão Sistólica": "115",
        "Pressão Diastólica": "75",
        "Glicose": "90"
    }
    func_c = classifica_entrada(fake_dados)
    assert "Batimentos: Normal" in func_c
    assert "Pressão: Normal" in func_c
    assert "Glicose: Normal" in func_c

'''
teste triste classifica dados
'''
def test_classifica_entrada_s():
    fake_dados = {
        "Batimentos": "abccba",
        "Pressão Sistólica": "115",
        "Pressão Diastólica": "75",
        "Glicose": "90"
    }
    try:
        classifica_entrada(fake_dados)
    except ValueError:
        assert True


''' 
casos felizes da função verifica_inteiro
'''
def test_verifica_inteiro_h():
    assert verifica_inteiro(42) is True
    assert verifica_inteiro("42") is True
    assert verifica_inteiro(4.2) is True
    assert verifica_inteiro(" 042 ") is True


''' 
casos tristes da função verifica_inteiro
'''
def test_verifica_inteiro_s():
    assert verifica_inteiro("33aa") is False
    assert verifica_inteiro("33.a3") is False
    assert verifica_inteiro("aaa") is False
    assert verifica_inteiro("") is False
    assert verifica_inteiro(" ") is False


if __name__ == "__main__":
    suite = TestSuite([
        FunctionTestCase(test_verifica_inteiro_h),
        FunctionTestCase(test_verifica_inteiro_s),
        FunctionTestCase(test_recebe_dados_h),
        FunctionTestCase(test_recebe_dados_stop),
        FunctionTestCase(test_recebe_dados_keyboard),
        FunctionTestCase(test_classifica_entrada_h),
        FunctionTestCase(test_classifica_entrada_s)

    ])

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
