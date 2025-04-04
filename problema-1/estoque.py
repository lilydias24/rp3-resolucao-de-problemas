import json
import os
from datetime import datetime 

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
            dados = {'pessoas': {}}
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
        elif tipo_dado == 'date':
            try:
                return datetime.strptime(entrada, '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                print('<<<--- Formato de data inválido! Use o formato AAAA-MM-DD. --->>>')
        else: 
            if entrada.strip():
                return entrada
            else:
                print(f'<<<--- Formato de dado inválido! Tente novamente. --->>>')

def create_produto(nome_prod, descricao, valor, quant_estoque, nivel_min):
    """Cadastra um novo produto no estoque evitando duplicatas."""
    
    dados = transportar_dados('estoque.json')
    produtos = dados.get('produtos', {})

    if produtos: 
        max_id = max(int(m) for m in produtos.keys())
        novo_id = str(max_id + 1)
    else: 
        novo_id = '1' 

    
    """ Adiciona o novo produto ao dicionário"""
    produtos[novo_id] = {
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
    print(f'<<<--- Produto cadastrado com sucesso! ID atribuído: {novo_id} --->>>')

def create_pessoa(pessoa_id, tipo_pessoa, nome, status, doc, cep, contato):
    """Cadastra uma nova pessoa no estoque evitando duplicatas."""
    
    dados = transportar_dados('pessoas.json')
    pessoas = dados.get('pessoas', {})

    """Converte o ID para string para garantir que a busca ocorra corretamente """
    pessoa_id_str = str(pessoa_id)

    if pessoa_id_str in pessoas:  
        print(f'<<<--- Erro: Já existe uma pessoa cadastrada com o ID {pessoa_id}! --->>>')
        return
    
    """ Adiciona a nova pessoa ao dicionário"""
    pessoas[pessoa_id_str] = {
        'tipo_pessoa' : tipo_pessoa,
        'nome': nome,
        'status': status,
        'doc': doc,
        'cep': cep,
        'contato': contato
    }

    """ Atualiza o JSON com o novo pessoa """
    dados['pessoas'] = pessoas
    salvar_dados('pessoas.json', dados)
    print(f'<<<--- Pessoa com ID {pessoa_id} cadastrada com sucesso! --->>>')

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
        print('\n <<<--- Nenhum produto cadastrado no sistema. --->>>')
        return

    print('\n\t <<<--- Produtos em Estoque --->>>')
    print('\n')
    for id_produto, produto in produtos.items():
        print(f'\t ID: {id_produto} | Nome: {produto['nome']} | Estoque Atual: {produto['quant_estoque']}')
