from .estoque import transportar_dados


def listar_niveis():
    """Lista todos os produtos cadastrados no estoque e verifica o nível mínimo."""
    
    dados = transportar_dados('estoque.json')
    produtos = dados.get('produtos', {})

    if not produtos:
        print('\n <<<--- Nenhum produto cadastrado no sistema. --->>>')
        return

    print('\n\t <<<--- Produtos em  Estoque : --->>>\n')
    
    for produto_id, produto in produtos.items():
        print(f'ID: {produto_id}')
        print(f'Nome: {produto["nome"]}')
        print(f'Descrição: {produto["descricao"]}')
        print(f'Valor: R$ {produto["valor"]:.2f}')
        print(f'Quantidade em Estoque: {produto["quant_estoque"]}')
        print(f'Nível Mínimo: {produto["nivel_min"]}')
        
        # verificação do nível mínimo
        if produto["quant_estoque"] <= produto["nivel_min"]:
            print("⚠️  ALERTA: Estoque abaixo do nível mínimo!")
        
        print('-' * 30)

# rodando a função para listar os produtos e alertar sobre estoques baixos
def main():
    print("\n\t<<<--- Lista de Níveis do Estoque  --->>>")
    listar_niveis()

if __name__ == '__main__':
    main()

