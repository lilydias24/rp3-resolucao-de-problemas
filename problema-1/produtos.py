import json

produtos_arq = "problema-1\\produtos.json"

# Conexão com armazenamento de produtos no JSON
def transportar_dados():
    try : 
        with open(produtos_arq, 'r') as dados :
            return json.load(dados)
    except FileNotFoundError:
        return []

# Armazenamento dos produtos no JSON
def salvar_dados(produtos): 
    with open(produtos_arq, 'w') as dados:
        json.dump(produtos, dados, indent=4) 

# Verificação do tipo de dado inserido.
def validar_dado(tipo_dado, mensagem) : 
    while True:
        entrada = input(mensagem)
        if tipo_dado == 'int':
            if entrada.isdigit():
                return int(entrada)
            else: 
                print('<<<--- Formato de dado inválido! Tente novamente com um valor inteiro --->>>')
        elif tipo_dado == 'float':
            try:
                return float(entrada)
            except ValueError:
                print('<<<--- Formato de dado inválido! Tente novamente com um valor decimal --->>>')
        else: # No caso de strings
            if entrada.strip():
                return entrada
            else:
                print('<<<--- Formato de dado inválido! Tente novamente. --->>>')

# Cadastramento de produtos no JSON
def cadastrar_produto():
    produtos = transportar_dados()

    # Verificação do ID
    produto_id = validar_dado('int', 'ID do Produto : ')
    if any(produto['ID'] == produto_id for produto in produtos) :
        print('<<<--- ID duplicado! Tente novamente com um ID único. --->>>')
        return

    nome_prod =  validar_dado('str', 'Nome : ')
    descricao =  validar_dado('str', 'Descrição : ')
    valor =  validar_dado('float', 'Valor : ')
    quant_estoque =  validar_dado('int', 'Quantidade em Estoque : ')
    nivel_min =  validar_dado('int', 'Nível Mínimo de Estoque : ')

    produtos.append({
        'ID' : produto_id, 
        'nome' : nome_prod, 
        'descricao' : descricao, 
        'valor' : valor, 
        'quant_estoque' : quant_estoque, 
        'nivel_min' : nivel_min
    })
    salvar_dados(produtos)
    print('\n <<<--- Produto cadastrado com sucesso! --->>>')

# Listagem dos produtos previamente cadastrados
def listar_produto():
    produtos = transportar_dados()
    if produtos:
        for produto in produtos:
            print (produto)
    else:
         print('\n <<<--- Nenhum produto cadastrado no sistema. --->>>')

# Atualização de dados dos produtos existentes
def atualizar_produto():
    produtos = transportar_dados()
    produto_id = validar_dado('int', 'Informe o ID do produto que deseja atualizar : ')
    for produto in produtos:
        if produto['ID'] == produto_id:
            produto['nome'] =  validar_dado('str', 'Informe o novo nome do produto : ')
            produto['descricao'] =  validar_dado('str', 'Informe a nova descrição do produto : ') 
            produto['valor'] =  validar_dado('float', 'Informe o novo valor do produto : ')
            produto['quant_estoque'] =  validar_dado('int', 'Informe a nova quantidade de produto em estoque : ') # Integrar com a entrada e saída de produtos.
            produto['nivel_min'] =  validar_dado('int', 'Informe a nova quantidade mínima para o produto no estoque : ') # Integrar com o controle de nível de estoque e função alerta.
            salvar_dados(produtos)
            print('\n <<<--- Registro do produto atualizado com sucesso! --->>>')
            return
    print('\n <<<--- Produto não encontrado no sistema. --->>>')

# Deleção de produtos existentes   
def deletar_produto():
    produtos = transportar_dados()
    produto_id = validar_dado('int', 'Informe o ID do produto que deseja deletar : ')

    produtos = [produto for produto in produtos if produto['ID']!= produto_id]
    salvar_dados(produtos)
    print('\n <<<--- Produto deletado com sucesso! --->>>')
    # consultar grupo sobre ação de deletar por modificação de status em ativo > inativo

# Index de acesso as opções disponíveis para os produtos
def main():
    while True: 
        print('\n\t <<<--- Gerenciar Produtos --->>> ')
        print('\n\t 1. Cadastrar Produto')
        print('\t 2. Visualizar Produtos')
        print('\t 3. Atualizar Produto')
        print('\t 4. Deletar Produto')
        print('\t 5. Sair')
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
            print('Retornando...')
            break
        else : 
            print('Opção Inválida, tente novamente.')

if __name__ == '__main__' :
    main()