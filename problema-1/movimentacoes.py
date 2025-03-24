import json
from datetime import datetime

produtos_arq = "problema-1\\produtos.json"
movimentacoes_arq = "problema-1\\movimentacoes.json"

# Conexão com JSON's
def transportar_dados(arquivo):
    try:
        with open(arquivo, 'r') as dados:
            return json.load(dados)
    except FileNotFoundError:
        return []

# Armazenamento dos dados no JSON
def salvar_dados(arquivo, dados):
    with open(arquivo, 'w') as arq:
        json.dump(dados, arq, indent=4)

# Geração de ID único automático, para evitar conflitos
def gerar_id(movimentacoes):
    if not movimentacoes:
        return 1  # Retorna 1 se a lista estiver vazia
    maior_id = max(movimento['id_movimento'] for movimento in movimentacoes)
    return maior_id + 1  # Retorna o próximo ID disponível

# Verificação do tipo de dado inserido.
def validar_dado(tipo_dado, mensagem):
    while True:
        entrada = input(mensagem)
        if tipo_dado == 'int':
            if entrada.isdigit():
                return int(entrada)
            else:
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
            if entrada.strip():
                return entrada
            else:
                print('<<<--- Formato de dado inválido! Insira um valor não vazio. --->>>')

# Registro de movimentações no JSON
def registrar_movimentacao():
    produtos = transportar_dados(produtos_arq)
    movimentacoes = transportar_dados(movimentacoes_arq)

    # Verificação do ID
    id_produto = validar_dado('int', 'ID do Produto: ')
    if not any(produto['ID'] == id_produto for produto in produtos):
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

    movimentacoes.append(nova_movimentacao)
    salvar_dados(movimentacoes_arq, movimentacoes)
    print('\n <<<--- Movimentação cadastrada com sucesso! --->>>')

# Listagem das movimentações previamente registradas
def listar_movimentacoes():
    movimentacoes = transportar_dados(movimentacoes_arq)
    if movimentacoes:
        for movimentacao in movimentacoes:
            print(movimentacao)
    else:
        print('\n <<<--- Nenhuma movimentação registrada no sistema. --->>>')

# Deleção de movimentações existentes   
def deletar_movimentacao():
    movimentacoes = transportar_dados(movimentacoes_arq)
    movimentacao_id = validar_dado('int', 'Informe o ID da movimentação que deseja deletar : ')

    movimentacoes = [movimentacao for movimentacao in movimentacoes if movimentacao['id_movimento']!= movimentacao_id]
    salvar_dados(movimentacoes_arq, movimentacoes)
    print('\n <<<--- Movimentação deletada com sucesso! --->>>')
    # consultar grupo sobre ação de deletar por modificação de status em ativo > inativo

def main():
    while True:
        print('\n\t <<<--- Gerenciar Movimentações --->>> ')
        print('\n\t 1. Cadastrar Movimentação')
        print('\t 2. Listar Movimentações')
        print('\t 3. Deletar Movimentação')
        print('\t 4. Sair')
        print('\n\t <<< ------------------------ >>> ')

        opcao = input('\n > Selecione uma opção: ')

        if opcao == '1':
            registrar_movimentacao()
        elif opcao == '2':
            listar_movimentacoes()
        elif opcao == '3':
            deletar_movimentacao()
        elif opcao == '4':
            print('Retornando...')
            break
        else:
            print('Opção inválida, tente novamente.')

if __name__ == '__main__':
    main()
