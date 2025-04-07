import os
import json
import estoque
import produtos

CAMINHO_JSON = os.path.join(os.path.dirname(__file__), 'estoque.json')

def test_cadastrar_produto(monkeypatch):
    entradas = iter([
        "Produto Teste",      # nome
        "Descrição Teste",    # descrição
        "19.99",              # valor
        "10",                 # quantidade
        "2"                   # nível mínimo
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(entradas))

    produtos.cadastrar_produto()

    dados = estoque.transportar_dados("estoque.json")
    produtos_dict = dados.get("produtos", {})

    assert len(produtos_dict) > 0

    ultimo_id = str(max(int(k) for k in produtos_dict.keys()))
    produto = produtos_dict[ultimo_id]

    assert produto["nome"] == "Produto Teste"
    assert produto["descricao"] == "Descrição Teste"
    assert produto["valor"] == 19.99
    assert produto["quant_estoque"] == 10
    assert produto["nivel_min"] == 2

def test_listar_produto(capsys):
    produtos.listar_produto()
    captured = capsys.readouterr()
    assert "Produtos Cadastrados no Estoque" in captured.out

def test_atualizar_produto(monkeypatch):
    dados = estoque.transportar_dados("estoque.json")
    produtos_dict = dados.get("produtos", {})
    if not produtos_dict:
        raise Exception("Nenhum produto para atualizar.")

    ultimo_id = str(max(int(k) for k in produtos_dict.keys()))
    produto_antigo = produtos_dict[ultimo_id]

    entradas = iter([
        ultimo_id,            # ID
        "Produto Alterado",   # nome
        "",                   # descrição (mantém)
        "29.90",              # valor
        "",                   # quantidade (mantém)
        "5"                   # nível mínimo
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(entradas))

    produtos.atualizar_produto()

    dados_atualizados = estoque.transportar_dados("estoque.json")
    produto = dados_atualizados['produtos'][ultimo_id]

    assert produto['nome'] == "Produto Alterado"
    assert produto['valor'] == 29.90
    assert produto['nivel_min'] == 5
    assert produto['descricao'] == produto_antigo['descricao']  # permaneceu
    assert produto['quant_estoque'] == produto_antigo['quant_estoque']  # permaneceu

def test_deletar_produto(monkeypatch):
    dados = estoque.transportar_dados("estoque.json")
    produtos_dict = dados.get("produtos", {})
    if not produtos_dict:
        raise Exception("Nenhum produto para deletar.")

    ultimo_id = str(max(int(k) for k in produtos_dict.keys()))
    nome_produto = produtos_dict[ultimo_id]['nome']

    entradas = iter([
        ultimo_id,  # ID
        "s"         # confirmação
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(entradas))

    produtos.deletar_produto()

    dados_atualizados = estoque.transportar_dados("estoque.json")
    assert ultimo_id not in dados_atualizados['produtos']
