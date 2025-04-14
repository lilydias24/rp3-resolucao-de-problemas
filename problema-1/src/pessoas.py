from src import estoque
from estilo import print_terminal

def cadastrar_pessoa():
    print_terminal('\t 1 - Cadastrar Cliente', cor='amarelo', estilo='negrito')
    print_terminal('\t 2 - Cadastrar Fornecedor', cor='amarelo', estilo='negrito')
    escolha = estoque.validar_dado('str', 'Informe o tipo de pessoa que deseja cadastrar: ').strip()
    
    if escolha == '1' :
        tipo_pessoa = 'cliente'
        nome = estoque.validar_dado('str', 'Nome: ')
        doc = estoque.validar_dado('int', 'CPF: ')
    elif escolha == '2' : 
        tipo_pessoa = 'fornecedor'
        nome = estoque.validar_dado('str', 'Razão social: ')
        doc = estoque.validar_dado('int', 'CNPJ: ')
    else:
        print_terminal(f'\n <<<--- Formato de dado inválido, tente novamente. --->>>', cor='amarelo', estilo='normal')
        return
    
    status = estoque.validar_dado('str', 'status: ')
    cep = estoque.validar_dado('int', 'CEP: ')
    contato = estoque.validar_dado('int', 'Contato: ')
    
    estoque.create_pessoa(tipo_pessoa, nome, status, doc, cep, contato)

def listar_pessoas():
        dados = estoque.transportar_dados('pessoas.json')
        pessoas = dados.get('pessoas', {})
        
        if not pessoas: 
            print_terminal(f'\n <<<--- Nenhuma pessoa cadastrada no sistema. --->>>', cor='vermelho', estilo='normal')
            return
        
        print_terminal("\n <<<--- Pessoas cadastradas no sistema : --->>> \n", cor='verde', estilo='negrito')
        
        for pessoa_id, pessoa in pessoas.items():
            print_terminal('-' * 30, cor='branco', estilo='negrito')
            print_terminal(f'ID: {pessoa_id}', cor='branco', estilo='negrito')
            print_terminal(f'Tipo de Pessoa: {pessoa["tipo_pessoa"]}', cor='branco', estilo='negrito')
            
            if pessoa['tipo_pessoa'] == 'cliente':
                print_terminal(f'Nome: {pessoa["nome"]}', cor='branco', estilo='negrito')
                print_terminal(f'CPF: {pessoa["cpf"]}', cor='branco', estilo='negrito')
            else:
                print_terminal(f'Razão Social: {pessoa["razao_social"]}', cor='branco', estilo='negrito')
                print_terminal(f'CNPJ: {pessoa["cnpj"]}', cor='branco', estilo='negrito')
            
            print_terminal(f'Status: {pessoa["status"]}', cor='branco', estilo='negrito')
            print_terminal(f'CEP: {pessoa["cep"]}', cor='branco', estilo='negrito')
            print_terminal(f'Contato: {pessoa["contato"]}', cor='branco', estilo='negrito')
            print_terminal('-' * 30, cor='branco', estilo='negrito')

def alterar_pessoa():
     
    dados = estoque.transportar_dados('pessoas.json')
    pessoas = dados.get('pessoas', {})

    pessoa_id = estoque.validar_dado('int', 'Informe o ID da pessoa que deseja alterar: ')
    pessoa_id_str = str(pessoa_id)  

    if pessoa_id_str not in pessoas:
        print_terminal(f'\n <<<--- Pessoa não encontrada no sistema. --->>>', cor='vermelho', estilo='normal')
        return

    pessoa = pessoas[pessoa_id_str] 

    print_terminal("\n Deixe o campo vazio para manter o valor atual.", cor='amarelo', estilo='negrito')
    
    if pessoa['tipo_pessoa'] == 'cliente':
        novo_nome = input(f'Novo Nome ({pessoa["nome"]}): ').strip()
        novo_doc = input(f'Novo CPF ({pessoa["cpf"]}): ').strip()
    else:  
        novo_nome = input(f'Nova Razão Social ({pessoa["razao_social"]}): ').strip()
        novo_doc = input(f'Novo CNPJ ({pessoa["cnpj"]}): ').strip()

    novo_status = input(f'Novo Status ({pessoa["status"]}): ').strip()
    novo_cep = input(f'Novo CEP ({pessoa["cep"]}): ').strip()
    novo_contato = input(f'Novo Contato ({pessoa["contato"]}): ').strip()

    """ Apenas altera os valores que foram preenchidos """
    if novo_nome:
        if pessoa['tipo_pessoa'] == 'cliente':
            pessoa['nome'] = novo_nome
        else:
            pessoa['razao_social'] = novo_nome

    if novo_doc.isdigit():
        if pessoa['tipo_pessoa'] == 'cliente':
            pessoa['cpf'] = int(novo_doc)
        else:
            pessoa['cnpj'] = int(novo_doc)

    if novo_status:
        pessoa['status'] = novo_status
    if novo_cep.isdigit():
        pessoa['cep'] = int(novo_cep)
    if novo_contato.isdigit():
        pessoa['contato'] = int(novo_contato)

    estoque.salvar_dados('pessoas.json', dados)
    print_terminal(f'\n <<<--- Registro de ({pessoa['tipo_pessoa']}) atualizado com sucesso! --->>>', cor='verde', estilo='negrito')
    

def excluir_pessoa():
    
    dados = estoque.transportar_dados('pessoas.json')
    pessoas = dados.get('pessoas', {})

    pessoa_id = estoque.validar_dado('int', 'Informe o ID da pessoa que deseja deletar: ')
    pessoa_id_str = str(pessoa_id)  

    if pessoa_id_str not in pessoas:
        print_terminal('\n <<<--- Pessoa não encontrada no sistema. --->>>', cor='vermelho', estilo='normal')
        return

    pessoa = pessoas.get(pessoa_id_str, None)
    
    if not pessoa:
        print_terminal('\n <<<--- Erro ao acessar pessoa. --->>>', cor='vermelho', estilo='negrito')
        return

    """ Confirmar antes de excluir """
    confirmacao = input(f'Tem certeza que deseja excluir a pessoa "{pessoa.get('nome', '?')}"? (s/n): ').strip().lower()
    if confirmacao != 's':
        print_terminal('\n <<<--- Operação cancelada. --->>>', cor='amarelo', estilo='negrito')
        return

    del pessoas[pessoa_id_str]
    dados['pessoas'] = pessoas
    estoque.salvar_dados('pessoas.json', dados)

    print_terminal('\n <<<--- Pessoa removida com sucesso! --->>>', cor='verde', estilo='negrito')

""" Index de acesso as opções disponíveis para as pessoas """
def main():
    while True: 
        print_terminal('.-.' * 25, cor='ciano', estilo='negrito')
        print_terminal('\n | \t\t<<<--- Gerenciar Pessoas --->>> \t\t |\n', cor='ciano', estilo='negrito')
        print_terminal('.-.' * 25, cor='ciano', estilo='negrito')
        
        print_terminal('\n\t 1. Cadastrar Pessoa', cor='roxo', estilo='negrito')
        print_terminal('\n\t\t 2. Visualizar Pessoas', cor='roxo', estilo='negrito')
        print_terminal('\n\t\t 3. Alterar Pessoa', cor='roxo', estilo='negrito')
        print_terminal('\n\t\t 4. Excluir Pessoa', cor='roxo', estilo='negrito')
        print_terminal('\n\t\t 5. Voltar ao Início', cor='roxo', estilo='negrito')
        print_terminal('.-.' * 25, cor='ciano', estilo='negrito')
        
        opcao = input('\n\t\033[1;32m >>> Selecione uma das opções acima: \033[0m').strip()
        print_terminal('.-.' * 25, cor='ciano', estilo='negrito')
        
        if opcao == '1' :
            cadastrar_pessoa()
        elif opcao == '2' :
            listar_pessoas()
        elif opcao == '3' :
            alterar_pessoa()
        elif opcao == '4' :
            excluir_pessoa()
        elif opcao == '5' :
            return 
        else : 
            print_terminal('Opção Inválida, tente novamente.')

if __name__ == '__main__' :
    main()