import json
import os

dir_base = os.path.dirname(os.path.abspath(__file__))  
# json_dir = os.path.join(dir_base, 'estoque.json')

def transportar_dados(name_json):
    """Carrega os dados do arquivo JSON necesário
    - Verifica se existe o arquivo disponível
    - se não cria um dicionário adequado ao contexto.
    """

    dir_json = os.path.join(dir_base, name_json)

    if os.path.exists(dir_json):
        with open(dir_json, 'r', encoding='utf-8') as file:
            dados = json.load(file)
    else: 
        if name_json == 'estoque.json':
            dados = {'produtos': {}}
        elif name_json == 'movimentacoes.json':
            dados = {'movimentacoes': []}
        elif name_json == 'pessoas.json':
            dados = {'clientes': {}, 'fornecedores': {}}
        else:
            print(f'Não foi possível realizar a conexão dos dados com o armazenamento.')
            return
    return dados

def salvar_dados(name_json, dados):
    """Salva os dados no arquivo JSON de acordo com o contexto"""

    dir_json = os.path.join(dir_base, name_json)
    
    with open(dir_json, 'w', encoding='utf-8') as file:
        json.dump(dados, file, indent=4, ensure_ascii=False)

# Funções auxiliares para manipulação do estoque

def validar_dado(tipo_dado, mensagem) : 
    """ Verifica o tipo de dado inserido pelo usuário."""
    
    while True:
        entrada = input(mensagem)
        if tipo_dado == 'int':
            if entrada.isdigit():
                return int(entrada)
            else: 
                print(f'<<<--- Formato de dado inválido! Tente novamente com um valor inteiro --->>>')
        elif tipo_dado == 'float':
            try:
                return float(entrada)
            except ValueError:
                print(f'<<<--- Formato de dado inválido! Tente novamente com um valor decimal --->>>')
        else: 
            if entrada.strip():
                return entrada
            else:
                print(f'<<<--- Formato de dado inválido! Tente novamente. --->>>')

def create_produto(produto_id, nome_prod, descricao, valor, quant_estoque, nivel_min):
    """Cadastra um novo produto no estoque evitando duplicatas."""
    
    dados = transportar_dados('estoque.json')
    produtos = dados.get('produtos', {})

    """Converte o ID para string para garantir que a busca ocorra corretamente """
    produto_id_str = str(produto_id)

    if produto_id_str in produtos:  
        print(f'<<<--- Erro: Já existe um produto cadastrado com o ID {produto_id}! --->>>')
        return
    
    """ Adiciona o novo produto ao dicionário"""
    produtos[produto_id_str] = {
        'nome': nome_prod,
        'descricao': descricao,
        'valor': valor,
        'quant_estoque': quant_estoque,
        'nivel_min': nivel_min,
        'entradas' : [],
        'saidas' : []
    }

    """ Atualiza o JSON com os novos produtos """
    dados['produtos'] = produtos
    salvar_dados('estoque.json', dados)
    print(f'<<<--- Produto com ID {produto_id} cadastrado com sucesso! --->>>')

def create_cliente(cliente_id, nome, status, cpf, cep, contato):
    """Cadastra um novo cliente no estoque evitando duplicatas."""
    
    dados = transportar_dados('pessoas.json')
    clientes = dados.get('clientes', {})

    """Converte o ID para string para garantir que a busca ocorra corretamente """
    cliente_id_str = str(cliente_id)

    if cliente_id_str in clientes:  
        print(f'<<<--- Erro: Já existe um cliente cadastrado com o ID {cliente_id}! --->>>')
        return
    
    """ Adiciona o novo cliente ao dicionário"""
    clientes[cliente_id_str] = {
        'nome': nome,
        'status': status,
        'cpf': cpf,
        'cep': cep,
        'contato': contato
    }

    """ Atualiza o JSON com o novo cliente """
    dados['clientes'] = clientes
    salvar_dados('pessoas.json', dados)
    print(f'<<<--- CLiente com ID {cliente_id} cadastrado com sucesso! --->>>')

def create_fornecedor(fornecedor_id, razao_social, status, cnpj, cep, contato):
    """Cadastra um novo fornecedor no estoque evitando duplicatas."""
    
    dados = transportar_dados('pessoas.json')
    fornecedores = dados.get('fornecedores', {})

    """Converte o ID para string para garantir que a busca ocorra corretamente """
    fornecedor_id_str = str(fornecedor_id)

    if fornecedor_id_str in fornecedores:  
        print(f'<<<--- Erro: Já existe um fornecedor cadastrado com o ID {fornecedor_id}! --->>>')
        return
    
    """ Adiciona o novo fornecedor ao dicionário"""
    fornecedores[fornecedor_id_str] = {
        'razao_social': razao_social,
        'status': status,
        'cnpj': cnpj,
        'cep': cep,
        'contato': contato
    }

    """ Atualiza o JSON com o novo fornecedor """
    dados['fornecedores'] = fornecedores
    salvar_dados('pessoas.json', dados)
    print(f'<<<--- Fornecedor com ID {fornecedor_id} cadastrado com sucesso! --->>>')

def registrar_movimentacao(tipo, codigo, quantidade, fornecedor=None, cliente=None):
    """Registra as entradas e/ou saídas de um produto."""
    
    dados = transportar_dados('movimentacoes.json')

    if tipo == 'entrada':
        from entrada import registrar_entrada
        registrar_entrada(codigo, quantidade)
    elif tipo == 'saida':
        from saida import registrar_saida
        registrar_saida(codigo, quantidade)
    else: 
        print(f'<<<--- Tipo de movimentação inválida! Use "entrada" ou saida". --->>>')
        return

    movimentacao = {
        'tipo': tipo,
        'codigo': codigo,
        'quantidade': quantidade,
        'fornecedor': fornecedor,
        'cliente': cliente
    }
    
    dados['movimentacoes'].append(movimentacao)
    salvar_dados('movimentacoes.json', dados)

    print(f'<<<--- Movimentação registrada: {tipo} de {quantidade} unidades do produto {codigo}. --->>>')

def listar_estoque():
    """Lista todos os produtos e suas quantidades disponíveis em estoque"""

    dados = transportar_dados('estoque.json')
    produtos = dados.get('produtos', {})

    if not produtos:
        print("\n <<<--- Nenhum produto cadastrado no sistema. --->>>")
        return

    print("\n <<<--- Produtos em Estoque --->>>")
    for id_produto, produto in produtos.items():
        print(f"ID: {id_produto} | Nome: {produto['nome']} | Estoque Atual: {produto['quant_estoque']}")
