import json
import os

def transportar_dados():
    """Carrega os dados do arquivo JSON estoque.json
    - Verifica se existe o arquivo estoque.json disponível
    - se não cria um dicionário vazio."""

    if os.path.exists('estoque.json'):
        with open('estoque.json', 'r', encoding='utf-8') as file:
            dados = json.load(file)
    else: 
        dados = {'produtos': {}, 'movimentacoes': []}

    for produto in dados.get('produtos', {}).values():
        produto.setdefault('entradas', [])
        produto.setdefault('saidas', [])

    return dados

def salvar_dados(dados):
    """Salva os dados no arquivo JSON estoque.json."""
    
    with open('estoque.json', 'w', encoding='utf-8') as file:
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
    
    dados = transportar_dados()
    movimentacoes = dados.get('movimentacoes', [])
    movimentacoes.append(movimentacao)
    
    dados['movimentacoes'] = movimentacoes
    salvar_dados(dados)
    print(f'<<<--- Movimentação registrada: {tipo} de {quantidade} unidades do produto {codigo}. --->>>')

def gerar_relatorio():
    """Gera um relatório das movimentações em formato CSV."""
    
    import csv
    dados = transportar_dados()
    produtos = dados.get('produtos', {})

    with open('relatorio.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Tipo', 'Código', 'Quantidade', 'Data'])
        
        for mov in dados.get('movimentacoes', []):
            writer.writerow([mov['tipo_movimento'], mov['id_produto'], mov['quantidade'], mov['data']])

    print(f'Relatório gerado com sucesso!')