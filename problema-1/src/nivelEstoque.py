from .estoque import transportar_dados
from estilo import print_terminal



def listar_niveis():
    """Lista todos os produtos cadastrados no estoque e verifica o nível mínimo."""
    
    dados = transportar_dados('estoque.json')
    produtos = dados.get('produtos', {})

    if not produtos:
        print_terminal('\n <<<--- Nenhum produto cadastrado no sistema. --->>>', cor='amarelo', estilo='normal')
        return

    print_terminal('\n\t <<<--- Produtos em  Estoque : --->>>\n', cor='amarelo', estilo='negrito')
    
    for produto_id, produto in produtos.items():
        print_terminal(f'ID: {produto_id}', cor='branco', estilo='negrito')
        print_terminal(f'Nome: {produto["nome"]}', cor='branco', estilo='negrito')
        print_terminal(f'Descrição: {produto["descricao"]}', cor='branco', estilo='negrito')
        print_terminal(f'Valor: R$ {produto["valor"]:.2f}', cor='branco', estilo='negrito')
        print_terminal(f'Quantidade em Estoque: {produto["quant_estoque"]}', cor='branco', estilo='negrito')
        print_terminal(f'Nível Mínimo: {produto["nivel_min"]}', cor='branco', estilo='negrito')
        
        if produto["quant_estoque"] <= produto["nivel_min"]:
            print_terminal("⚠️  ALERTA: Estoque abaixo do nível mínimo!", cor='vermelho', estilo='normal')
        
        print_terminal('-' * 30, cor='amarelo', estilo='normal')

def main():
    print_terminal("\n\t<<<--- Lista de Níveis do Estoque  --->>>", cor='amarelo', estilo='negrito')
    listar_niveis()

if __name__ == '__main__':
    main()

