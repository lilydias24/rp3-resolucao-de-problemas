import pytest
from unittest.mock import patch
from movimentacoes import gerar_id, validar_dado, deletar_movimentacao, registrar_movimentacao


def test_gerar_id():
    movimentacoes = [
        {"id_movimento": 1},
        {"id_movimento": 2},
        {"id_movimento": 5}
    ]
    assert gerar_id(movimentacoes) == 6  # Deve retornar o próximo ID disponível
    assert gerar_id([]) == 1  # Deve retornar 1 se a lista estiver vazia


@patch("builtins.input")
def test_validar_dado(mock_input):
    mock_input.side_effect = ["10", "10.5", "2024-03-29", "teste"]
    assert validar_dado("int", "") == 10
    assert validar_dado("float", "") == 10.5
    assert validar_dado("date", "") == "2024-03-29"
    assert validar_dado("str", "") == "teste"


@patch("movimentacoes.transportar_dados")
@patch("movimentacoes.salvar_dados")
@patch("entrada.registrar_entrada")
@patch("saida.registrar_saida")
@patch("builtins.input")
def test_registrar_movimentacao(mock_input, mock_registrar_saida, mock_registrar_entrada, mock_salvar_dados, mock_transportar_dados):
    mock_transportar_dados.return_value = {"produtos": {"1": {"estoque": 10}}, "movimentacoes": []}
    mock_input.side_effect = ["1", "2", "Cliente", "saida", "5", "2025-04-27"]

    registrar_movimentacao()
    mock_salvar_dados.assert_called()


@patch("movimentacoes.transportar_dados")
@patch("movimentacoes.salvar_dados")
@patch("builtins.input")
def test_deletar_movimentacao(mock_input, mock_salvar_dados, mock_transportar_dados):
    dados_mock = {"movimentacoes": [{"id_movimento": 1}, {"id_movimento": 2}]}
    mock_transportar_dados.return_value = dados_mock
    mock_input.return_value = "1"

    deletar_movimentacao()
    mock_salvar_dados.assert_called()