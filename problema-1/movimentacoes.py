from relatorio import gerar_relatorio
from estoque import transportar_dados, salvar_dados, listar_estoque
from entrada import registrar_entrada
from saida import registrar_saida
from datetime import datetime

def gerar_id(movimentacoes):
    """ Gera ID único automático, para evitar conflitos"""
    
    if not movimentacoes:
        return 1  # Retorna 1 se a lista estiver vazia
    maior_id = max(movimento['id_movimento'] for movimento in movimentacoes)
    return maior_id + 1  # Retorna o próximo ID disponível

def validar_dado(tipo_dado, mensagem):
    """ Verifica o tipo de dado inserido."""
    
    while True:
        entrada = input(mensagem).strip()
        if tipo_dado == 'int':
            if entrada.isdigit():
                return int(entrada)
            print('<<<--- Formato de dado inválido! Insira um valor inteiro. --->>>')
        elif tipo_dado == 'float':
            try:
                return float(entrada)
            except ValueError:
                print('<<<--- Formato de dado inválido! Insira um valor decimal. --->>>')
        elif tipo_dado == 'date':
            try:
                return datetime.strptime(entrada, '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                print('<<<--- Formato de data inválido! Use o formato AAAA-MM-DD. --->>>')
        else:  # Para strings
            if entrada:
                return entrada
            print('<<<--- Formato de dado inválido! Insira um valor não vazio. --->>>')

def registrar_movimentacao():
    """ Registro de movimentações no JSON """
    
    dados = transportar_dados()
    produtos = dados.get('produtos', {})
    movimentacoes = dados.get('movimentacoes', [])

    id_produto = str(validar_dado('int', 'ID do Produto: '))
    if id_produto not in produtos:
        print('\n <<<--- Produto não encontrado no sistema! --->>>')
        return

    id_pessoa = validar_dado('int', 'ID da Pessoa (Cliente ou Fornecedor): ')
    tipo_pessoa = validar_dado('str', 'Tipo de Pessoa (Cliente/Fornecedor): ').lower()
    tipo_movimento = validar_dado('str', 'Tipo de Movimento (Entrada/Saída): ').lower()
    quantidade = validar_dado('int', 'Quantidade: ')
    data = validar_dado('date', 'Data da Movimentação (AAAA-MM-DD): ')

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
    dados['movimentacoes'] = movimentacoes
    salvar_dados(dados)
    print('\n <<<--- Movimentação cadastrada com sucesso! --->>>')

def listar_movimentacoes():
    """ Listagem das movimentações previamente registradas """

    movimentacoes = transportar_dados().get('movimentacoes', [])
    
    if movimentacoes:
        for movimentacao in movimentacoes:
            print(movimentacao)
    else:
        print('\n <<<--- Nenhuma movimentação registrada no sistema. --->>>')

def deletar_movimentacao():
    """ Deleção de movimentações existentes """

    dados = transportar_dados()
    movimentacoes = dados.get('movimentacoes', [])
    movimentacao_id = validar_dado('int', 'Informe o ID da movimentação que deseja deletar : ')

    nova_mov = [mov for mov in movimentacoes if mov['id_movimento'] != movimentacao_id]
    
    if len(nova_mov) == len(movimentacoes):
        print(f'\n <<<--- ID da movimentação não encontrado. Nenhuma alteração foi feita. --->>> ')
        return
    
    dados['movimentacoes'] = nova_mov
    salvar_dados(dados)
    print('\n <<<--- Movimentação deletada com sucesso! --->>>')
    # consultar grupo sobre ação de deletar por modificação de status em ativo > inativo

def main():
    while True:
        print('\n\t <<<--- Gerenciar Movimentações --->>> ')
        print('\n\t 1. Cadastrar Movimentação')
        print('\t 2. Listar Movimentações')
        print('\t 3. Deletar Movimentação')
        print('\t 4. Visualizar Estoque Atual')
        print('\t 5. Gerar Relatório de Movimentações')
        print('\t 6. Sair')
        print('\n\t <<< ------------------------ >>> ')

        opcao = input('\n > Selecione uma opção: ')

        if opcao == '1':
            registrar_movimentacao()
        elif opcao == '2':
            listar_movimentacoes()
        elif opcao == '3':
            deletar_movimentacao()
        elif opcao == '4':
            listar_estoque()
        elif opcao == '5':
            gerar_relatorio()
        elif opcao == '6':
            print('Retornando...')
            break
        else:
            print('Opção inválida, tente novamente.')

if __name__ == '__main__':
    main()
