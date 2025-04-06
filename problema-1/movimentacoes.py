from relatorio import gerar_relatorio
from entrada import registrar_entrada
from saida import registrar_saida
from pesquisa import pesquisar_movimentacoes
from nivelEstoque import listar_niveis
from datetime import datetime
import estoque

def gerar_id(movimentacoes):
    """ Gera ID único automático, para evitar conflitos"""
    
    if not movimentacoes:
        return 1  # Retorna 1 se a lista estiver vazia
    maior_id = max(movimento['id_movimento'] for movimento in movimentacoes)
    return maior_id + 1  # Retorna o próximo ID disponível

def registrar_movimentacao():
    """ Registro de movimentações no JSON """
    
    dados1 = estoque.transportar_dados('estoque.json')
    produtos = dados1.get('produtos', {})
    dados2 = estoque.transportar_dados('movimentacoes.json')
    movimentacoes = dados2.get('movimentacoes', [])

    id_produto = str(estoque.validar_dado('int', 'ID do Produto: '))
    if id_produto not in produtos:
        print('\n <<<--- Produto não encontrado no sistema! --->>>')
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
        print(f'\n <<<--- Tipo de movimento inválido! --->>>') 
        return

    movimentacoes.append(nova_movimentacao)
    dados2['movimentacoes'] = movimentacoes
    estoque.salvar_dados('movimentacoes.json', dados2)
    print('\n <<<--- Movimentação cadastrada com sucesso! --->>>')

def listar_movimentacoes():
    """ Listagem das movimentações previamente registradas """

    movimentacoes = estoque.transportar_dados('movimentacoes.json').get('movimentacoes', [])
    
    if movimentacoes:
        for movimentacao in movimentacoes:
            print(movimentacao)
    else:
        print('\n <<<--- Nenhuma movimentação registrada no sistema. --->>>')

def deletar_movimentacao():
    """ Deleção de movimentações existentes """

    dados = estoque.transportar_dados('movimentacoes.json')
    movimentacoes = dados.get('movimentacoes', [])
    movimentacao_id = estoque.validar_dado('int', 'Informe o ID da movimentação que deseja deletar : ')

    nova_mov = [mov for mov in movimentacoes if mov['id_movimento'] != movimentacao_id]
    
    if len(nova_mov) == len(movimentacoes):
        print(f'\n <<<--- ID da movimentação não encontrado. Nenhuma alteração foi feita. --->>> ')
        return
    
    dados['movimentacoes'] = nova_mov
    estoque.salvar_dados('movimentacoes.json', dados)
    print('\n <<<--- Movimentação deletada com sucesso! --->>>')
    # consultar grupo sobre ação de deletar por modificação de status em ativo > inativo

def main():
    while True:
        print('\n\t <<<--- Gerenciar Movimentações --->>> ')
        print('\n\t 1. Verificar Níveis do Estoque Atual')
        print('\t 2. Cadastrar Movimentação')
        print('\t 3. Listar Movimentações')
        print('\t 4. Deletar Movimentação')
        print('\t 5. Buscar Registros de Movimentações.')
        print('\t 6. Voltar ao Início')
        print('\n\t <<< ------------------------ >>> ')

        opcao = input('\n > Selecione uma opção: ')

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
            print('.' * 20)
            break
        else:
            print('Opção inválida, tente novamente.')

if __name__ == '__main__':
    main()
