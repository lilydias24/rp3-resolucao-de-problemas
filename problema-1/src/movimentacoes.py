from .relatorio import gerar_relatorio
from .entrada import registrar_entrada
from .saida import registrar_saida
from .pesquisa import pesquisar_movimentacoes
from .nivelEstoque import listar_niveis
from datetime import datetime
from src import estoque
from estilo import print_terminal

def gerar_id(movimentacoes):
    """ Gera ID único automático, para evitar conflitos"""
    
    if not movimentacoes:
        return 1  
    maior_id = max(movimento['id_movimento'] for movimento in movimentacoes)
    return maior_id + 1  

def registrar_movimentacao():
    """ Registro de movimentações no JSON """
    
    dados1 = estoque.transportar_dados('estoque.json')
    produtos = dados1.get('produtos', {})
    dados2 = estoque.transportar_dados('movimentacoes.json')
    movimentacoes = dados2.get('movimentacoes', [])

    id_produto = str(estoque.validar_dado('int', 'ID do Produto: '))
    if id_produto not in produtos:
        print_terminal('\n <<<--- Produto não encontrado no sistema! --->>>', cor='vermelho', estilo='normal')
        return

    id_pessoa = estoque.validar_dado('int', 'ID da Pessoa (Cliente ou Fornecedor): ')
    tipo_pessoa = estoque.validar_dado('str', 'Tipo de Pessoa (Cliente/Fornecedor): ').lower()
    tipo_movimento = estoque.validar_dado('str', 'Tipo de Movimento (Entrada/Saída): ').lower()
    quantidade = estoque.validar_dado('int', 'Quantidade: ')
    data = estoque.validar_dado('date', 'Data da Movimentação (AAAA-MM-DD): ')

    id_movimento = gerar_id(movimentacoes)
    nova_movimentacao = {
        'id_movimento': id_movimento,
        'id_produto': id_produto,
        'id_pessoa': id_pessoa,
        'tipo_pessoa': tipo_pessoa,
        'tipo_movimento': tipo_movimento,
        'quantidade': quantidade,
        'data': data
    }

    if tipo_movimento in ['entrada']:
        registrar_entrada(id_produto, quantidade)
    elif tipo_movimento in ['saida']:
        registrar_saida(id_produto, quantidade)
    else:
        print_terminal(f'\n <<<--- Tipo de movimento inválido! --->>>', cor='vermelho', estilo='normal') 
        return

    movimentacoes.append(nova_movimentacao)
    dados2['movimentacoes'] = movimentacoes
    estoque.salvar_dados('movimentacoes.json', dados2)
    print_terminal('\n <<<--- Movimentação cadastrada com sucesso! --->>>', cor='verde', estilo='normal')

def listar_movimentacoes():
    """ Listagem das movimentações previamente registradas """

    movimentacoes = estoque.transportar_dados('movimentacoes.json').get('movimentacoes', [])
    
    if movimentacoes:
        for movimentacao in movimentacoes:
            print(movimentacao)
    else:
        print_terminal('\n <<<--- Nenhuma movimentação registrada no sistema. --->>>', cor='amarelo', estilo='normal')

def deletar_movimentacao():
    """ Deleção de movimentações existentes """

    dados = estoque.transportar_dados('movimentacoes.json')
    movimentacoes = dados.get('movimentacoes', [])
    movimentacao_id = estoque.validar_dado('int', 'Informe o ID da movimentação que deseja deletar : ')

    nova_mov = [mov for mov in movimentacoes if mov['id_movimento'] != movimentacao_id]
    
    if len(nova_mov) == len(movimentacoes):
        print_terminal(f'\n <<<--- ID da movimentação não encontrado. Nenhuma alteração foi feita. --->>> ', cor='amarelo', estilo='normal')
        return
    
    dados['movimentacoes'] = nova_mov
    estoque.salvar_dados('movimentacoes.json', dados)
    print_terminal('\n <<<--- Movimentação deletada com sucesso! --->>>', cor='verde', estilo='normal')

def main():
    while True:
        print_terminal('.-.' * 25, cor='ciano', estilo='negrito')
        print_terminal('\n | \t\t<<<--- Gerenciar Movimentações --->>> \t\t |\n', cor='ciano', estilo='negrito')
        print_terminal('.-.' * 25, cor='ciano', estilo='negrito')
        
        print_terminal('\n\n\t\t 1. Verificar Níveis do Estoque Atual', cor='roxo', estilo='negrito')
        print_terminal('\n\t\t 2. Cadastrar Movimentação', cor='roxo', estilo='negrito')
        print_terminal('\n\t\t 3. Listar Movimentações', cor='roxo', estilo='negrito')
        print_terminal('\n\t\t 4. Deletar Movimentação', cor='roxo', estilo='negrito')
        print_terminal('\n\t\t 5. Buscar Registros de Movimentações.', cor='roxo', estilo='negrito')
        print_terminal('\n\t\t 6. Voltar ao Início', cor='roxo', estilo='negrito')
        print_terminal('.-.' * 25, cor='ciano', estilo='negrito')

        opcao = input('\n\t\033[1;32m >>> Selecione uma das opções acima: \033[0m').strip()
        print_terminal('.-.' * 25, cor='ciano', estilo='negrito')

        if opcao == '1':
            listar_niveis()
        elif opcao == '2':
            registrar_movimentacao()
        elif opcao == '3':
            listar_movimentacoes()
        elif opcao == '4':
            deletar_movimentacao()
        elif opcao == '5':
            pesquisar_movimentacoes()
        elif opcao == '6':
            break
        else:
            print_terminal('Opção inválida, tente novamente.', cor='vermelho', estilo='normal')
            continue

if __name__ == '__main__':
    main()
