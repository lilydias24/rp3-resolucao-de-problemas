from datetime import datetime
from .estoque import transportar_dados, salvar_dados


def registrar_saida(id_produto, quantidade):
    """Registra a saída de um produto no estoque"""

    dados = transportar_dados('estoque.json')
    produtos = dados.get('produtos', {})

    if id_produto not in produtos:
        print(f"produto com ID {id_produto} não encontrado no estoque.")
        return
    
    produto = produtos[id_produto]
    total_em_estoque = produto['quant_estoque']
    
    if quantidade <= 0:
        print("Quantidade inválida. Insira um valor positivo.")
        return
    
    if total_em_estoque < quantidade:
        print(f'Estoque do produto insuficiente para remover {quantidade} unidades.')
        return

    saida = {
        'quantidade': quantidade,
        'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    produto['saidas'].append(saida)
    produto['quant_estoque'] -= quantidade 
    salvar_dados('estoque.json', dados)
    
    print(f"\n \t | Saída registrada em {saida['data']}: {quantidade} unidades do produto {id_produto}. |")
    print(f"\n \t | Novo estoque do produto {id_produto}: {produto['quant_estoque']} |")

