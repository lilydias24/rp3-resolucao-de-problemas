import json
import os

dir = os.path.dirname(os.path.abspath(__file__))  
json_dir = os.path.join(dir, 'estoque.json')

def transportar_dados():
    """Carrega os dados do arquivo JSON estoque.json
    - Verifica se existe o arquivo estoque.json disponível
    - se não cria um dicionário vazio."""

    if os.path.exists(json_dir):
        with open(json_dir, 'r', encoding='utf-8') as file:
            dados = json.load(file)
    else: 
        dados = {'produtos': {}, 'movimentacoes': []}

    for produto in dados.get('produtos', {}).values():
        produto.setdefault('entradas', [])
        produto.setdefault('saidas', [])

    return dados

def salvar_dados(dados):
    """Salva os dados no arquivo JSON estoque.json"""
    
    with open(json_dir, 'w', encoding='utf-8') as file:
        json.dump(dados, file, indent=4, ensure_ascii=False)

# Funções auxiliares para manipulação do estoque

def create_produto(produto_id, nome_prod, descricao, valor, quant_estoque, nivel_min):
    """Cadastra um novo produto no estoque evitando duplicatas."""
    
    dados = transportar_dados()
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
    salvar_dados(dados)
    print(f'<<<--- Produto com ID {produto_id} cadastrado com sucesso! --->>>')

def registrar_movimentacao(tipo, codigo, quantidade, fornecedor=None, cliente=None):
    """Registra as entradas e/ou saídas de um produto."""
    
    dados = transportar_dados()

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
    salvar_dados(dados)

    print(f'<<<--- Movimentação registrada: {tipo} de {quantidade} unidades do produto {codigo}. --->>>')

def listar_estoque():
    """Lista todos os produtos e suas quantidades disponíveis em estoque"""

    dados = transportar_dados()
    produtos = dados.get('produtos', {})

    if not produtos:
        print("\n <<<--- Nenhum produto cadastrado no sistema. --->>>")
        return

    print("\n <<<--- Produtos em Estoque --->>>")
    for id_produto, produto in produtos.items():
        print(f"ID: {id_produto} | Nome: {produto['nome']} | Estoque Atual: {produto['quant_estoque']}")  # ✅ **Nova função adicionada**
