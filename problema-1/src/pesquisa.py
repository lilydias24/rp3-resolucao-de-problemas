from .estoque import transportar_dados
from estilo import print_terminal

def pesquisar_movimentacoes():

    estoque = transportar_dados("estoque.json")
    movimentacoes = transportar_dados("movimentacoes.json")
    pessoas_data = transportar_dados("pessoas.json")

    produtos = estoque.get("produtos", {})
    movimentos = movimentacoes.get("movimentacoes", [])
    pessoas = pessoas_data.get("pessoas", {})

    produtos_com_movimentos = {mov["id_produto"] for mov in movimentos}

    for produto_id in produtos_com_movimentos:
        produto = produtos.get(produto_id)
        if not produto:
            continue

        nome = produto.get("nome", "N/A")
        descricao = produto.get("descricao", "N/A")
        valor = produto.get("valor", "N/A")
        quant_estoque = produto.get("quant_estoque", "N/A")

        print_terminal(f"ID Produto: {produto_id}", cor='branco', estilo='negrito')
        print_terminal(f"Nome: {nome}", cor='branco', estilo='negrito')
        print_terminal(f"Descrição: {descricao}", cor='branco', estilo='negrito')
        print_terminal(f"Valor: {valor}", cor='branco', estilo='negrito')
        print_terminal(f"Quantidade em Estoque: {quant_estoque}", cor='branco', estilo='negrito')
        print_terminal("\nMovimentações Relacionadas:", cor='branco', estilo='negrito')

        for movimento in movimentos:
            if movimento["id_produto"] == produto_id:
                id_pessoa = str(movimento.get("id_pessoa"))
                pessoa = pessoas.get(id_pessoa)

                if not pessoa:
                    continue

                tipo_pessoa = pessoa.get("tipo_pessoa", "N/A")

                if tipo_pessoa == "cliente":
                    nome_ou_razao = pessoa.get("nome", "N/A")
                elif tipo_pessoa == "fornecedor":
                    nome_ou_razao = pessoa.get("razao_social", "N/A")
                else:
                    nome_ou_razao = "N/A"

                id_movimento = movimento.get("id_movimento", "N/A")
                tipo_movimento = movimento.get("tipo_movimento", "N/A")
                quantidade = movimento.get("quantidade", "N/A")
                data = movimento.get("data", "N/A")

                print_terminal(f"  - ID Movimento: {id_movimento}", cor='branco', estilo='negrito')
                print_terminal(f"    Tipo: {tipo_movimento}", cor='branco', estilo='negrito')
                print_terminal(f"    Quantidade: {quantidade}", cor='branco', estilo='negrito')
                print_terminal(f"    Data: {data}", cor='branco', estilo='negrito')
                print_terminal(f"    Tipo de Pessoa: {tipo_pessoa}", cor='branco', estilo='negrito')
                print_terminal(f"    Nome/Razão Social: {nome_ou_razao}", cor='branco', estilo='negrito')

        print_terminal("-" * 40, cor='branco', estilo='negrito')

def main():
    print_terminal("\n\t<<<--- Pesquisa de Produtos com Movimentações --->>>", cor='ciano', estilo='negrito')
    pesquisar_movimentacoes()

if __name__ == '__main__':
    main()