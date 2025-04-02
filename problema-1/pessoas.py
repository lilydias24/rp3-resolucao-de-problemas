import estoque

def listar_clientes():
        dados = estoque.transportar_dados('pessoas.json')
        clientes = dados.get('clientes', {})
        
        if not clientes: 
            print(f'\n <<<--- Nenhum cliente cadastrado no sistema. --->>>')
            return
        
        print("\n <<<--- Clientes cadastrados no sistema : --->>> \n")
        
        for cliente_id, cliente in clientes.items():
            print('-' * 30)
            print(f'ID: {cliente_id}')
            print(f'Nome: {cliente['nome']}')
            print(f'Status: {cliente['status']}')
            print(f'CPF: {cliente['cpf']}')
            print(f'CEP: {cliente['cep']}')
            print(f'Contato: {cliente['contato']}')
            print('-' * 30)

def cadastrar_cliente():

    cliente_id = estoque.validar_dado('int', 'ID do Cliente: ')
    nome = estoque.validar_dado('str', 'Nome: ')
    status = estoque.validar_dado('str', 'status: ')
    cpf = estoque.validar_dado('int', 'CPF: ')
    cep = estoque.validar_dado('int', 'CEP: ')
    contato = estoque.validar_dado('int', 'Contato: ')

    estoque.create_cliente(cliente_id, nome, status, cpf, cep, contato)

def alterar_cliente():
     
    dados = estoque.transportar_dados('pessoas.json')
    clientes = dados.get('clientes', {})

    cliente_id = estoque.validar_dado('int', 'Informe o ID do cliente que deseja alterar: ')
    cliente_id_str = str(cliente_id)  

    if cliente_id_str not in clientes:
        print(f'\n <<<--- Cliente não encontrado no sistema. --->>>')
        return

    cliente = clientes[cliente_id_str] 

    print("\n Deixe o campo vazio para manter o valor atual.")

    novo_nome = input(f'Novo nome ({cliente['nome']}): ').strip()
    novo_status = input(f'Novo status ({cliente['status']}): ').strip()
    novo_cpf = input(f'Novo cpf ({cliente['cpf']}): ').strip()
    novo_cep = input(f'Nova cep ({cliente['cep']}): ').strip()
    novo_contato = input(f'Novo contato ({cliente['contato']}): ').strip()

    """ Apenas altera os valores que foram preenchidos """
    if novo_nome:
        cliente['nome'] = novo_nome
    if novo_status:
        cliente['status'] = novo_status
    if novo_cpf.isdigit():
        cliente['cpf'] = int(novo_cpf)
    if novo_cep.isdigit():
        cliente['cep'] = int(novo_cep)
    if novo_contato.isdigit():
        cliente['contato'] = int(novo_contato)

    estoque.salvar_dados('pessoas.json', dados)
    print('\n <<<--- Registro do cliente atualizado com sucesso! --->>>')

def excluir_cliente():
    
    dados = estoque.transportar_dados('pessoas.json')
    clientes = dados.get('clientes', {})

    cliente_id = estoque.validar_dado('int', 'Informe o ID do Cliente que deseja deletar: ')
    cliente_id_str = str(cliente_id)  

    if cliente_id_str not in clientes:
        print('\n <<<--- Cliente não encontrado no sistema. --->>>')
        return

    cliente = clientes.get(cliente_id_str, None)
    
    if not cliente:
        print('\n <<<--- Erro ao acessar o cliente. --->>>')
        return

    """ Confirmar antes de excluir """
    confirmacao = input(f'Tem certeza que deseja excluir o cliente "{cliente.get('nome', 'Desconhecido')}"? (s/n): ').strip().lower()
    if confirmacao != 's':
        print('\n <<<--- Operação cancelada. --->>>')
        return

    del clientes[cliente_id_str]
    dados['clientes'] = clientes
    estoque.salvar_dados('pessoas.json', dados)

    print('\n <<<--- Cliente removido com sucesso! --->>>')

def listar_fornecedores():
        dados = estoque.transportar_dados('pessoas.json')
        fornecedores = dados.get('fornecedores', {})
        
        if not fornecedores: 
            print(f'\n <<<--- Nenhum fornecedor cadastrado no sistema. --->>>')
            return
        
        print("\n <<<--- Fornecedores cadastrados no sistema : --->>> \n")
        
        for fornecedor_id, fornecedor in fornecedores.items():
            print('-' * 30)
            print(f'ID: {fornecedor_id}')
            print(f'Razão Social: {fornecedor['razao_social']}')
            print(f'Status: {fornecedor['status']}')
            print(f'CNPJ: {fornecedor['cnpj']}')
            print(f'CEP: {fornecedor['cep']}')
            print(f'Contato: {fornecedor['contato']}')
            print('-' * 30)

def cadastrar_fornecedor():

    fornecedor_id = estoque.validar_dado('int', 'ID do Fornecedor: ')
    razao_social = estoque.validar_dado('str', 'Razão Social: ')
    status = estoque.validar_dado('str', 'Status: ')
    cnpj = estoque.validar_dado('int', 'CNPJ: ')
    cep = estoque.validar_dado('int', 'CEP: ')
    contato = estoque.validar_dado('int', 'Contato: ')

    estoque.create_fornecedor(fornecedor_id, razao_social, status, cnpj, cep, contato)

def alterar_fornecedor():
     
    dados = estoque.transportar_dados('pessoas.json')
    fornecedores = dados.get('fornecedores', {})

    fornecedor_id = estoque.validar_dado('int', 'Informe o ID do fornecedor que deseja alterar: ')
    fornecedor_id_str = str(fornecedor_id)  

    if fornecedor_id_str not in fornecedores:
        print(f'\n <<<--- Fornecedor não encontrado no sistema. --->>>')
        return

    fornecedor = fornecedores[fornecedor_id_str] 

    print("\n Deixe o campo vazio para manter o valor atual.")

    novo_razao = input(f'Nova Razão Social ({fornecedor['razao_social']}): ').strip()
    novo_status = input(f'Novo Status ({fornecedor['status']}): ').strip()
    novo_cnpj = input(f'Novo CNPJ ({fornecedor['cnpj']}): ').strip()
    novo_cep = input(f'Novo CEP ({fornecedor['cep']}): ').strip()
    novo_contato = input(f'Novo Contato ({fornecedor['contato']}): ').strip()

    """ Apenas altera os valores que foram preenchidos """
    if novo_razao:
        fornecedor['razao_social'] = novo_razao
    if novo_status:
        fornecedor['status'] = novo_status
    if novo_cnpj.isdigit():
        fornecedor['cnpj'] = int(novo_cnpj)
    if novo_cep.isdigit():
        fornecedor['cep'] = int(novo_cep)
    if novo_contato.isdigit():
        fornecedor['contato'] = int(novo_contato)

    estoque.salvar_dados('pessoas.json', dados)
    print('\n <<<--- Registro do fornecedor atualizado com sucesso! --->>>')

def excluir_fornecedor():
    
    dados = estoque.transportar_dados('pessoas.json')
    fornecedores = dados.get('fornecedores', {})

    fornecedor_id = estoque.validar_dado('int', 'Informe o ID do fornecedor que deseja deletar: ')
    fornecedor_id_str = str(fornecedor_id)  

    if fornecedor_id_str not in fornecedores:
        print('\n <<<--- Fornecedor não encontrado no sistema. --->>>')
        return

    fornecedor = fornecedores.get(fornecedor_id_str, None)
    
    if not fornecedor:
        print('\n <<<--- Erro ao acessar o fornecedor. --->>>')
        return

    """ Confirmar antes de excluir """
    confirmacao = input(f'Tem certeza que deseja excluir o fornecedor "{fornecedor.get('nome', 'Desconhecido')}"? (s/n): ').strip().lower()
    if confirmacao != 's':
        print('\n <<<--- Operação cancelada. --->>>')
        return

    del fornecedores[fornecedor_id_str]
    dados['fornecedores'] = fornecedores
    estoque.salvar_dados('pessoas.json', dados)

    print('\n <<<--- Fornecedor removido com sucesso! --->>>')

""" Index de acesso as opções disponíveis para as pessoas """
def main():
    while True: 
        print('\n\t <<<--- Gerenciar Clientes --->>> ')
        print('\n\t 1. Visualizar Clientes')
        print('\t 2. Cadastrar Cliente')
        print('\t 3. Alterar Cliente')
        print('\t 4. Excluir Cliente')
        
        print('\n\t <<<--- Gerenciar Fornecedores --->>> ')
        print('\n\t 5. Visualizar Fornecedores')
        print('\t 6. Cadastrar Fornecedor')
        print('\t 7. Alterar Fornecedor')
        print('\t 8. Excluir Fornecedor')
        print('\n\t <<< -------------------------- >>> ')
        
        opcao = input('\n > Selecione uma das opções acima : ')

        if opcao == '1' :
            listar_clientes()
        elif opcao == '2' :
            cadastrar_cliente()
        elif opcao == '3' :
            alterar_cliente()
        elif opcao == '4' :
            excluir_cliente()
        elif opcao == '5' :
            listar_fornecedores()
        elif opcao == '6' :
            cadastrar_fornecedor()
        elif opcao == '7' :
            alterar_fornecedor()
        elif opcao == '8' :
            excluir_fornecedor()
        else : 
            print('Opção Inválida, tente novamente.')

if __name__ == '__main__' :
    main()