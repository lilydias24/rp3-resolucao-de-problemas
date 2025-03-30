import json
from datetime import datetime
from estoque import transportar_dados, salvar_dados

def registrar_entrada(id_produto, quantidade):
    """Registrar a entrada de um produto no estoque"""
    
    dados = transportar_dados()
    produtos = dados.get('produtos', {})

    if str(id_produto) not in produtos:
        print(f"Produto com ID {id_produto} não encontrado no estoque.")
        return

    produto = produtos[str(id_produto)]  # Busca o produto pelo ID (string)
    
    # Garante que a chave 'entradas' exista
    if 'entradas' not in produto:
        produto['entradas'] = []
    
    entrada = {
        'quantidade': quantidade,
        'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
        
    produto['entradas'].append(entrada)  
    produto['quant_estoque'] += quantidade  # Atualiza o estoque
    
    salvar_dados(dados)  # Salva os dados atualizados no JSON
    print(f"Entrada registrada: {quantidade} unidades do produto {id_produto}.")
