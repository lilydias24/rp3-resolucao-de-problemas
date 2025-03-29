import json

# Caminho do arquivo JSON
produtos = r"C:\Users\eriquito\Documentos\FACUL\SEMESTRE_3\RP_III\MARCO_I\grupo-05\problema-1\produtos.json"

# Função para carregar dados do JSON
def dados():
    try:
        with open(produtos, 'r', encoding="utf-8") as dadosprodutos:
            dados = json.load(dadosprodutos)  # Carrega os dados corretamente
            # print(dados)  # Exibe os dados carregados
            return dados
    except FileNotFoundError:
        print("Arquivo não encontrado. Retornando uma lista vazia.")
        return []
    
# Chamando a função para testar os dados do JSON
# dados()

# Função para verificar se um ID existe no JSON
def verificar_idproduto(idproduto):
    produtos_lista = dados()  # Carrega os dados do JSON

    for produto in produtos_lista:
        if produto.get("ID") == idproduto:  # Verifica se o ID existe
             print(f"Produto selecionado: {produto['nome']}")
             return True  # Retorna True se encontrar o ID

    print("ID do produto não encontrado. Tente novamente.")
    return False  # Retorna False se o ID não for encontrado

# Função para verificar se a quantidade do produto possui em estoque
def verificar_estoque(qtd):
    produtos_lista = dados()  # Carrega os dados do JSON

    for produto in produtos_lista:
        if produto.get("estoque") >= qtd :  # Verifica se tem quantidade disponível
            if produto.get("estoque") - qtd <= produto.get("estoque_min") :
                print(f"Produto está no limite de estoque mínimo, fazer reposição!")
            return True  # Retorna True se tiver quantidade disponível

        if produto.get("estoque") == 0 :
            print("Produto com estoque zerado") # Verifica se o estoque está zerado
            return False  # Retorna False se o produto estiver com estoque zerado

def realizarVenda():
    while True:  # Loop até um ID válido ser encontrado
        try:
            idproduto = int(input("Informe o ID do produto que deseja comprar: "))
            if verificar_idproduto(idproduto) == True:
                qtd = int(input("Informe a quantidade que deseja comprar: "))
                if verificar_estoque(qtd) == True:
                    print("ok")
        except ValueError:
            print("Por favor, digite um número válido.")
    
    verificar_idproduto()
    
realizarVenda()