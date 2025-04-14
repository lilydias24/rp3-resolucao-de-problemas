from src import estoque
from estilo import print_terminal

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
        print_terminal('\n <<<--- Nenhum produto cadastrado no sistema. --->>>', cor='vermelho', estilo='normal')
        return

    print_terminal('\n\t <<<--- Produtos Cadastrados no Estoque : --->>>\n', cor='ciano', estilo='negrito')
    
    for produto_id, produto in produtos.items():
        print_terminal(f'ID: {produto_id}', cor='branco', estilo='negrito')
        print_terminal(f'Nome: {produto['nome']}', cor='branco', estilo='negrito')
        print_terminal(f'Descrição: {produto['descricao']}', cor='branco', estilo='negrito')
        print_terminal(f'Valor: R$ {produto['valor']:.2f}', cor='branco', estilo='negrito')
        print_terminal(f'Quantidade em Estoque: {produto['quant_estoque']}', cor='branco', estilo='negrito')
        print_terminal(f'Nível Mínimo: {produto['nivel_min']}', cor='branco', estilo='negrito')
        print_terminal('-' * 30, cor='branco', estilo='negrito')

def atualizar_produto():
    """Atualiza os dados de um produto existente no estoque."""
    
    dados = estoque.transportar_dados('estoque.json')
    produtos = dados.get('produtos', {})

    produto_id = estoque.validar_dado('int', 'Informe o ID do produto que deseja atualizar: ')
    produto_id_str = str(produto_id)  

    if produto_id_str not in produtos:
        print_terminal(f'\n <<<--- Produto não encontrado no sistema. --->>>', cor='vermelho', estilo='normal')
        return

    produto = produtos[produto_id_str] 

    print_terminal("\n Deixe o campo vazio para manter o valor atual.", cor='amarelo', estilo='negrito')

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
    print_terminal('\n <<<--- Registro do produto atualizado com sucesso! --->>>', cor='verde', estilo='negrito')

def deletar_produto():
    """Remove um produto do estoque pelo ID."""
    
    dados = estoque.transportar_dados('estoque.json')
    produtos = dados.get('produtos', {})

    produto_id = estoque.validar_dado('int', 'Informe o ID do produto que deseja deletar: ')
    produto_id_str = str(produto_id)  

    if produto_id_str not in produtos:
        print_terminal('\n <<<--- Produto não encontrado no sistema. --->>>', cor='vermelho', estilo='normal')
        return

    produto = produtos.get(produto_id_str, None)
    
    if not produto:
        print_terminal('\n <<<--- Erro ao acessar o produto. --->>>', cor='vermelho', estilo='negrito')
        return

    """ Confirmar antes de excluir """
    confirmacao = input(f'Tem certeza que deseja excluir o produto "{produto.get('nome', 'Desconhecido')}"? (s/n): ').strip().lower()
    if confirmacao != 's':
        print_terminal('\n <<<--- Operação cancelada. --->>>', cor='amarelo', estilo='negrito')
        return

    del produtos[produto_id_str]
    dados['produtos'] = produtos
    estoque.salvar_dados('estoque.json', dados)

    print_terminal('\n <<<--- Produto removido com sucesso! --->>>', cor='verde', estilo='negrito')

""" Index de acesso as opções disponíveis para os produtos """
def main():
    while True: 
        print_terminal('.-.' * 25, cor='ciano', estilo='negrito')
        print_terminal('\n | \t\t<<<--- Gerenciar Produtos --->>> \t\t |\n', cor='ciano', estilo='negrito')
        print_terminal('.-.' * 25, cor='ciano', estilo='negrito')
        
        print_terminal('\n\n\t\t 1. Cadastrar Produto', cor='roxo', estilo='negrito')
        print_terminal('\n\t\t 2. Visualizar Produtos', cor='roxo', estilo='negrito')
        print_terminal('\n\t\t 3. Atualizar Produto', cor='roxo', estilo='negrito')
        print_terminal('\n\t\t 4. Deletar Produto', cor='roxo', estilo='negrito')
        print_terminal('\n\t\t 5. Voltar ao Início \n', cor='roxo', estilo='negrito')
        print_terminal('.-.' * 25, cor='ciano', estilo='negrito')

        opcao = input('\n\t\033[1;32m >>> Selecione uma das opções acima: \033[0m').strip()
        print_terminal('.-.' * 25, cor='ciano', estilo='negrito')

        if opcao == '1' :
            cadastrar_produto()
        elif opcao == '2' :
            listar_produto()
        elif opcao == '3' :
            atualizar_produto()
        elif opcao == '4' :
            deletar_produto()
        elif opcao == '5' :
            break
        else : 
            print_terminal('Opção inválida, tente novamente.', cor='vermelho', estilo='normal')
            continue

if __name__ == '__main__' :
    main()