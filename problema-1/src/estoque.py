import json
import os
<<<<<<< HEAD
<<<<<<< HEAD
from datetime import datetime 
from estilo import print_terminal
=======
=======
>>>>>>> bb34a614cd59ada5f53f0daf9f1fd5973152f4ff
from datetime import datetime

>>>>>>> bb34a614cd59ada5f53f0daf9f1fd5973152f4ff
dir_base = os.path.dirname(os.path.abspath(__file__))

def transportar_dados(name_json):
    """Carrega os dados do arquivo JSON necesário
    - Verifica se existe o arquivo disponível
    - se não cria um dicionário adequado ao contexto.
    """

    dir_json = os.path.join(dir_base,"..","data", name_json)

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
            print_terminal(f'Não foi possível realizar a conexão dos dados com o armazenamento.', cor='vermelho', estilo='normal')
            return
    return dados

def salvar_dados(name_json, dados):
    """Salva os dados no arquivo JSON de acordo com o contexto"""

    dir_json = os.path.join(dir_base,"..","data", name_json)
    
    with open(dir_json, 'w', encoding='utf-8') as file:
        json.dump(dados, file, indent=4, ensure_ascii=False)

def validar_dado(tipo_dado, mensagem) : 
    """ Verifica o tipo de dado inserido pelo usuário."""
    
    while True:
        entrada = input(mensagem)
        if tipo_dado == 'int':
            if entrada.isdigit():
                return int(entrada)
            else: 
                print_terminal(f'<<<--- Formato de dado inválido! Tente novamente com um valor inteiro --->>>', cor='amarelo', estilo='normal')
        elif tipo_dado == 'float':
            try:
                return float(entrada)
            except ValueError:
                print_terminal(f'<<<--- Formato de dado inválido! Tente novamente com um valor decimal --->>>', cor='amarelo', estilo='normal')
        elif tipo_dado == 'date':
            try:
                return datetime.strptime(entrada, '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                print_terminal('<<<--- Formato de data inválido! Use o formato AAAA-MM-DD. --->>>', cor='amarelo', estilo='normal')
        else: 
            if entrada.strip():
                return entrada
            else:
                print_terminal(f'<<<--- Formato de dado inválido! Tente novamente. --->>>', cor='amarelo', estilo='normal')

def create_produto(nome_prod, descricao, valor, quant_estoque, nivel_min):
    """Cadastra um novo produto no estoque evitando duplicatas."""
    
    dados = transportar_dados('estoque.json')
    produtos = dados.get('produtos', {})

    if produtos: 
        maior_id = max(int(maior) for maior in produtos.keys())
        novo_id = str(maior_id + 1)
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
    print_terminal(f'<<<--- Produto cadastrado com sucesso! ID atribuído: {novo_id} --->>>', cor='verde', estilo='normal')

def create_pessoa(tipo_pessoa, nome, status, doc, cep, contato):
    """Cadastra uma nova pessoa no estoque evitando duplicatas."""
    
    dados = transportar_dados('pessoas.json')
    pessoas = dados.get('pessoas', {})

    if pessoas: 
        maior_id = max(int(maior) for maior in pessoas.keys())
        novo_id = str(maior_id + 1)
    else: 
        novo_id = '1' 

    """Converte o ID para string para garantir que a busca ocorra corretamente """
    pessoa_id_str = str(novo_id)

    if pessoa_id_str in pessoas:  
        print_terminal(f'<<<--- Erro: Já existe uma pessoa cadastrada com o ID {pessoa_id_str}! --->>>', cor='vermelho', estilo='normal')
        return
    
    nova_pessoa = {
        'tipo_pessoa': tipo_pessoa,
        'status': status,
        'cep': cep,
        'contato': contato 
    }

    if tipo_pessoa == 'cliente':
        nova_pessoa['nome'] = nome
        nova_pessoa['cpf'] = doc
    else:
        nova_pessoa['razao_social'] = nome
        nova_pessoa['cnpj'] = doc

    """ Adiciona a nova pessoa ao dicionário"""
    pessoas[pessoa_id_str] = nova_pessoa

    dados['pessoas'] = pessoas
    salvar_dados('pessoas.json', dados)
    print_terminal(f'\n <<<--- {tipo_pessoa.capitalize()} cadastrado com sucesso! ID atribuído: {pessoa_id_str} --->>>', cor='verde', estilo='normal')

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
        print_terminal(f'<<<--- Tipo de movimentação inválida! Use "entrada" ou saida". --->>>', cor='amarelo', estilo='normal')
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

    print_terminal(f'<<<--- Movimentação registrada: {tipo} de {quantidade} unidades do produto {codigo}. --->>>', cor='verde', estilo='normal')

def listar_estoque():
    """Lista todos os produtos e suas quantidades disponíveis em estoque"""

    dados = transportar_dados('estoque.json')
    produtos = dados.get('produtos', {})

    if not produtos:
        print_terminal('\n <<<--- Nenhum produto cadastrado no sistema. --->>>', cor='amarelo', estilo='negrito')
        return

    print_terminal('-' * 30, cor='ciano', estilo='negrito')
    print_terminal('\n\t <<<--- Produtos em Estoque --->>>', cor='ciano', estilo='negrito')
    print_terminal('-' * 30, cor='ciano', estilo='negrito')
    
    for id_produto, produto in produtos.items():
        print_terminal(f'\t ID: {id_produto} | Nome: {produto['nome']} | Estoque Atual: {produto['quant_estoque']}', cor='verde', estilo='normal')

