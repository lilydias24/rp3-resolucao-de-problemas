from datetime import datetime
from .estoque import transportar_dados, salvar_dados
<<<<<<< HEAD
from estilo import print_terminal
=======
>>>>>>> bb34a614cd59ada5f53f0daf9f1fd5973152f4ff

def registrar_saida(id_produto, quantidade):
    """Registra a saída de um produto no estoque"""

    dados = transportar_dados('estoque.json')
    produtos = dados.get('produtos', {})

    if id_produto not in produtos:
        print_terminal(f"produto com ID {id_produto} não encontrado no estoque.", cor='vermelho', estilo='normal')
        return
    
    produto = produtos[id_produto]
    total_em_estoque = produto['quant_estoque']
    
    if quantidade <= 0:
        print_terminal("Quantidade inválida. Insira um valor positivo.", cor='amarelo', estilo='normal')
        return
    
    if total_em_estoque < quantidade:
        print_terminal(f'Estoque do produto insuficiente para remover {quantidade} unidades.', cor='vermelho', estilo='normal')
        return

    saida = {
        'quantidade': quantidade,
        'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    produto['saidas'].append(saida)
    produto['quant_estoque'] -= quantidade 
    salvar_dados('estoque.json', dados)
    
    print_terminal(f"\n \t | Saída registrada em {saida['data']}: {quantidade} unidades do produto {id_produto}. |", cor='verde', estilo='normal')
    print_terminal(f"\n \t | Novo estoque do produto {id_produto}: {produto['quant_estoque']} |", cor='verde', estilo='normal')

