from src import estoque

def cadastrar_produto():
    """Cadastra um novo produto no estoque evitando IDs duplicados."""
    
    nome_prod = estoque.validar_dado('str', 'Nome: ')
    descricao = estoque.validar_dado('str', 'Descrição: ')
    valor = estoque.validar_dado('float', 'Valor: ')
    quant_estoque = estoque.validar_dado('int', 'Quantidade em Estoque: ')
    nivel_min = estoque.validar_dado('int', 'Nível Mínimo de Estoque: ')

    estoque.create_produto(nome_prod, descricao, valor, quant_estoque, nivel_min)

def listar_produto():
    """Lista todos os produtos cadastrados no estoque."""
    
    dados = estoque.transportar_dados('estoque.json')
    produtos = dados.get('produtos', {})

    if not produtos:
        print('\n <<<--- Nenhum produto cadastrado no sistema. --->>>')
        return

    print('\n\t <<<--- Produtos Cadastrados no Estoque : --->>>\n')
    
    for produto_id, produto in produtos.items():
        print(f'ID: {produto_id}')
        print(f'Nome: {produto['nome']}')
        print(f'Descrição: {produto['descricao']}')
        print(f'Valor: R$ {produto['valor']:.2f}')
        print(f'Quantidade em Estoque: {produto['quant_estoque']}')
        print(f'Nível Mínimo: {produto['nivel_min']}')
        print('-' * 30)

def atualizar_produto():
    """Atualiza os dados de um produto existente no estoque."""
    
    dados = estoque.transportar_dados('estoque.json')
    produtos = dados.get('produtos', {})

    produto_id = estoque.validar_dado('int', 'Informe o ID do produto que deseja atualizar: ')
    produto_id_str = str(produto_id)  

    if produto_id_str not in produtos:
        print(f'\n <<<--- Produto não encontrado no sistema. --->>>')
        return

    produto = produtos[produto_id_str] 

    print("\n Deixe o campo vazio para manter o valor atual.")

    novo_nome = input(f'Novo nome ({produto['nome']}): ').strip()
    novo_descricao = input(f'Nova descrição ({produto['descricao']}): ').strip()
    novo_valor = input(f'Novo valor ({produto['valor']}): ').strip()
    novo_quantidade = input(f'Nova quantidade ({produto['quant_estoque']}): ').strip()
    novo_nivel_min = input(f'Novo nível mínimo ({produto['nivel_min']}): ').strip()

    """ Apenas altera os valores que foram preenchidos """
    if novo_nome:
        produto['nome'] = novo_nome
    if novo_descricao:
        produto['descricao'] = novo_descricao
    if novo_valor.replace('.', '', 1).isdigit():
        produto['valor'] = float(novo_valor)
    if novo_quantidade.isdigit():
        produto['quant_estoque'] = int(novo_quantidade)
    if novo_nivel_min.isdigit():
        produto['nivel_min'] = int(novo_nivel_min)

    estoque.salvar_dados('estoque.json', dados)
    print('\n <<<--- Registro do produto atualizado com sucesso! --->>>')

def deletar_produto():
    """Remove um produto do estoque pelo ID."""
    
    dados = estoque.transportar_dados('estoque.json')
    produtos = dados.get('produtos', {})

    produto_id = estoque.validar_dado('int', 'Informe o ID do produto que deseja deletar: ')
    produto_id_str = str(produto_id)  

    if produto_id_str not in produtos:
        print('\n <<<--- Produto não encontrado no sistema. --->>>')
        return

    produto = produtos.get(produto_id_str, None)
    
    if not produto:
        print('\n <<<--- Erro ao acessar o produto. --->>>')
        return

    """ Confirmar antes de excluir """
    confirmacao = input(f'Tem certeza que deseja excluir o produto "{produto.get('nome', 'Desconhecido')}"? (s/n): ').strip().lower()
    if confirmacao != 's':
        print('\n <<<--- Operação cancelada. --->>>')
        return

    del produtos[produto_id_str]
    dados['produtos'] = produtos
    estoque.salvar_dados('estoque.json', dados)

    print('\n <<<--- Produto removido com sucesso! --->>>')

""" Index de acesso as opções disponíveis para os produtos """
def main():
    while True: 
        print('\n\t <<<--- Gerenciar Produtos --->>> ')
        print('\n\t 1. Cadastrar Produto')
        print('\t 2. Visualizar Produtos')
        print('\t 3. Atualizar Produto')
        print('\t 4. Deletar Produto')
        print('\t 5. Voltar ao Início')
        print('\n\t <<< ------------------------ >>> ')

        opcao = input('\n > Selecione uma das opções acima : ')

        if opcao == '1' :
            cadastrar_produto()
        elif opcao == '2' :
            listar_produto()
        elif opcao == '3' :
            atualizar_produto()
        elif opcao == '4' :
            deletar_produto()
        elif opcao == '5' :
            print('.' * 20)
            break
        else : 
            print('Opção Inválida, tente novamente.')

if __name__ == '__main__' :
    main()