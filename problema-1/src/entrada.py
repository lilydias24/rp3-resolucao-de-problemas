from datetime import datetime
from .estoque import transportar_dados, salvar_dados
from estilo import print_terminal

def registrar_entrada(id_produto, quantidade):
    """Registrar a entrada de um produto no estoque"""
    
    dados = transportar_dados('estoque.json')
    produtos = dados.get('produtos', {})

    if str(id_produto) not in produtos:
        print_terminal(f"Produto com ID {id_produto} não encontrado no estoque.", cor='vermelho', estilo='normal')
        return

    produto = produtos[str(id_produto)]  
    
    entrada = {
        'quantidade': quantidade,
        'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
        
    produto['entradas'].append(entrada)  
    produto['quant_estoque'] += quantidade  
    
    salvar_dados('estoque.json', dados) 
    
    print_terminal(f"\n \t | Entrada registrada: {quantidade} unidades do produto {id_produto}. |", cor='verde', estilo='normal')
    print_terminal(f"\n \t | Novo estoque do produto {id_produto}: {produto['quant_estoque']} | ", cor='verde', estilo='normal') 

