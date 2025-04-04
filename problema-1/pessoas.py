import estoque

def listar_pessoas():
        dados = estoque.transportar_dados('pessoas.json')
        pessoas = dados.get('pessoas', {})
        
        if not pessoas: 
            print(f'\n <<<--- Nenhuma pessoa cadastrada no sistema. --->>>')
            return
        
        print("\n <<<--- Pessoas cadastradas no sistema : --->>> \n")
        
        for pessoa_id, pessoa in pessoas.items():
            print('-' * 30)
            print(f'ID: {pessoa_id}')
            print(f'Tipo de Pessoa: {pessoa['tipo_pessoa']}')
            print(f'Nome: {pessoa['nome']}')
            print(f'Status: {pessoa['status']}')
            print(f'Documento: {pessoa['doc']}')
            print(f'CEP: {pessoa['cep']}')
            print(f'Contato: {pessoa['contato']}')
            print('-' * 30)

def cadastrar_pessoa():

    pessoa_id = estoque.validar_dado('int', 'ID: ')

    print('1 - Cadastrar Cliente \n2 - Cadastrar Fornecedor')

    escolha = estoque.validar_dado('str', 'Informe o tipo de pessoa que deseja cadastrar: ').strip()
    
    if escolha == '1' :
        tipo_pessoa = 'cliente'
    elif escolha == '2' : 
        tipo_pessoa = 'fornecedor'
    else:
        print(f'\n <<<--- Formato de dado inválido, tente novamente. --->>>')
        return
    
    nome = estoque.validar_dado('str', 'Nome: ')
    status = estoque.validar_dado('str', 'status: ')
    doc = estoque.validar_dado('int', 'CPF ou CNPJ: ')
    cep = estoque.validar_dado('int', 'CEP: ')
    contato = estoque.validar_dado('int', 'Contato: ')
    
    estoque.create_pessoa(pessoa_id, tipo_pessoa, nome, status, doc, cep, contato)

def alterar_pessoa():
     
    dados = estoque.transportar_dados('pessoas.json')
    pessoas = dados.get('pessoas', {})

    pessoa_id = estoque.validar_dado('int', 'Informe o ID da pessoa que deseja alterar: ')
    pessoa_id_str = str(pessoa_id)  

    if pessoa_id_str not in pessoas:
        print(f'\n <<<--- Pessoa não encontrada no sistema. --->>>')
        return

    pessoa = pessoas[pessoa_id_str] 

    print("\n Deixe o campo vazio para manter o valor atual.")
    
    novo_nome = input(f'Novo Nome ({pessoa['nome']}): ').strip()
    novo_status = input(f'Novo Status ({pessoa['status']}): ').strip()
    novo_doc = input(f'Novo CPF ou CNPJ({pessoa['doc']}): ').strip()
    novo_cep = input(f'Novo CEP ({pessoa['cep']}): ').strip()
    novo_contato = input(f'Novo Contato ({pessoa['contato']}): ').strip()

    """ Apenas altera os valores que foram preenchidos """
    if novo_nome:
        pessoa['nome'] = novo_nome
    if novo_status:
        pessoa['status'] = novo_status
    if novo_doc.isdigit():
        pessoa['doc'] = int(novo_doc)
    if novo_cep.isdigit():
        pessoa['cep'] = int(novo_cep)
    if novo_contato.isdigit():
        pessoa['contato'] = int(novo_contato)

    estoque.salvar_dados('pessoas.json', dados)
    print(f'\n <<<--- Registro de ({pessoa['tipo_pessoa']}) atualizado com sucesso! --->>>')
    

def excluir_pessoa():
    
    dados = estoque.transportar_dados('pessoas.json')
    pessoas = dados.get('pessoas', {})

    pessoa_id = estoque.validar_dado('int', 'Informe o ID da pessoa que deseja deletar: ')
    pessoa_id_str = str(pessoa_id)  

    if pessoa_id_str not in pessoas:
        print('\n <<<--- Pessoa não encontrada no sistema. --->>>')
        return

    pessoa = pessoas.get(pessoa_id_str, None)
    
    if not pessoa:
        print('\n <<<--- Erro ao acessar pessoa. --->>>')
        return

    """ Confirmar antes de excluir """
    confirmacao = input(f'Tem certeza que deseja excluir a pessoa "{pessoa.get('nome', 'Desconhecido')}"? (s/n): ').strip().lower()
    if confirmacao != 's':
        print('\n <<<--- Operação cancelada. --->>>')
        return

    del pessoas[pessoa_id_str]
    dados['pessoas'] = pessoas
    estoque.salvar_dados('pessoas.json', dados)

    print('\n <<<--- Pessoa removida com sucesso! --->>>')

""" Index de acesso as opções disponíveis para as pessoas """
def main():
    while True: 
        print('\n\t <<<--- Gerenciar Pessoas --->>> ')
        print('\n\t 1. Visualizar Pessoas')
        print('\t 2. Cadastrar Pessoa')
        print('\t 3. Alterar Pessoa')
        print('\t 4. Excluir Pessoa')
        
        opcao = input('\n > Selecione uma das opções acima : ')

        if opcao == '1' :
            listar_pessoas()
        elif opcao == '2' :
            cadastrar_pessoa()
        elif opcao == '3' :
            alterar_pessoa()
        elif opcao == '4' :
            excluir_pessoa()
        elif opcao == '5' :
            print('Sair.')
            return 
        else : 
            print('Opção Inválida, tente novamente.')

if __name__ == '__main__' :
    main()