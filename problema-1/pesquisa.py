from estoque import transportar_dados


estoque = transportar_dados("estoque.json")
movimentacoes = transportar_dados("movimentacoes.json")


produtos = estoque.get("produtos", {})
movimentos = movimentacoes.get("movimentacoes", [])


produtos_com_movimentos = {mov["id_produto"] for mov in movimentos}


for produto_id in produtos_com_movimentos:
    produto = produtos.get(produto_id)
    
    if not produto:
        continue  

    nome = produto.get("nome", "N/A")
    descricao = produto.get("descricao", "N/A")
    valor = produto.get("valor", "N/A")
    quant_estoque = produto.get("quant_estoque", "N/A")

    print(f"ID Produto: {produto_id}")
    print(f"Nome: {nome}")
    print(f"Descrição: {descricao}")
    print(f"Valor: {valor}")
    print(f"Quantidade em Estoque: {quant_estoque}")


    print("\nMovimentações Relacionadas:")
    for movimento in movimentos:
        if movimento["id_produto"] == produto_id:
            id_movimento = movimento.get("id_movimento", "N/A")
            tipo_movimento = movimento.get("tipo_movimento", "N/A")
            quantidade = movimento.get("quantidade", "N/A")
            data = movimento.get("data", "N/A")

            print(f"  - ID Movimento: {id_movimento}")
            print(f"    Tipo: {tipo_movimento}")
            print(f"    Quantidade: {quantidade}")
            print(f"    Data: {data}")

    print("-" * 40)
