import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.administracao.gerenciarConta import (
    criar_conta,
    buscar_conta_por_id,
    editar_conta,
    excluir_conta,
    carregar_contas,
    salvar_contas,
    criar_conta_dict,
)

# Caminho para o arquivo contas.csv
CAMINHO_CONTAS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dados', 'contas.csv'))

def test_criar_conta():
    # Teste de criação de conta válida
    sucesso, mensagem = criar_conta(CAMINHO_CONTAS, "João", "joao@example.com", "senha1234")
    assert sucesso is True
    assert mensagem == "Conta criada com sucesso"

    contas = carregar_contas(CAMINHO_CONTAS)
    assert len(contas) == 1
    assert contas[0]["nome"] == "João"
    assert contas[0]["email"] == "joao@example.com"

    # Teste de criação de conta com email já existente
    sucesso, mensagem = criar_conta(CAMINHO_CONTAS, "Maria", "joao@example.com", "senha5678")
    assert sucesso is False
    assert mensagem == "Email já está em uso"

    # Teste de criação de conta com senha curta
    sucesso, mensagem = criar_conta(CAMINHO_CONTAS, "Ana", "ana@example.com", "123")
    assert sucesso is False
    assert mensagem == "A senha deve ter pelo menos 8 caracteres"


def test_buscar_conta_por_id():
    conta = buscar_conta_por_id(CAMINHO_CONTAS, "1")
    assert conta is not None
    assert conta["nome"] == "João"

    conta = buscar_conta_por_id(CAMINHO_CONTAS, "3")
    assert conta is None

def test_editar_conta():
    # Teste de edição de conta existente
    sucesso, mensagem = editar_conta(CAMINHO_CONTAS, "1", "João Silva", None, None)
    assert sucesso is True
    assert mensagem == "Conta atualizada com sucesso"

    contas = carregar_contas(CAMINHO_CONTAS)
    assert contas[0]["nome"] == "João Silva"

    # Teste de edição de conta inexistente
    sucesso, mensagem = editar_conta(CAMINHO_CONTAS, "3", "Ana", None, None)
    assert sucesso is False
    assert mensagem == "Conta não encontrada"

def test_excluir_conta():
    # Teste de exclusão de conta existente
    sucesso, mensagem = excluir_conta(CAMINHO_CONTAS, "1")
    assert sucesso is True
    assert mensagem == "Conta excluída com sucesso"

    # Teste de exclusão de conta inexistente
    sucesso, mensagem = excluir_conta(CAMINHO_CONTAS, "3")
    assert sucesso is False
    assert mensagem == "Conta não encontrada"
