import json

# Caminho do arquivo JSON
caminho_json = r"C:\Users\eriquito\Documentos\FACUL\SEMESTRE_3\RP_III\MARCO_I\grupo-05\problema-1\produtos.json"

# Função para carregar dados do JSON
def carregar_dados():
    try:
        with open(caminho_json, 'r', encoding="utf-8") as arquivo:
            return json.load(arquivo)  # Retorna os dados como lista de dicionários
    except FileNotFoundError:
        print("Arquivo não encontrado. Criando novo JSON...")
        return []  # Retorna uma lista vazia se o arquivo não existir

# Função para salvar os dados no JSON
def salvar_dados(lista_produtos): 
    with open(caminho_json, 'w', encoding="utf-8") as arquivo:
        json.dump(lista_produtos, arquivo, indent=4, ensure_ascii=False)  # Agora salva corretamente

# Função para verificar se um ID existe no JSON
def verificar_idproduto(idproduto):
    produtos_lista = carregar_dados()  # Carrega os dados do JSON

    for produto in produtos_lista:
        if produto.get("ID") == idproduto:  # Verifica se o ID existe
            print(f"✅ Produto selecionado: {produto['nome']}")
            return True  # Retorna True se encontrar o ID

    print("❌ ID do produto não encontrado. Tente novamente.")
    return False  # Retorna False se o ID não for encontrado

# Função para verificar e atualizar o estoque
def verificar_estoque(idproduto, qtd):
    produtos_lista = carregar_dados()  # Carrega os dados do JSON

    for produto in produtos_lista:
        if produto.get("ID") == idproduto:  # Confirma que é o produto certo
            estoque_atual = produto.get("estoque", 0)  # Obtém o estoque atual
            estoque_minimo = produto.get("estoque_min", 0)  # Obtém o estoque mínimo

            if estoque_atual < qtd:  # ❌ Se não houver estoque suficiente, impede a venda
                print(f"❌ Estoque insuficiente para {produto['nome']}. Disponível: {estoque_atual}.")
                return False

            # ✅ Atualiza o estoque somente se houver estoque suficiente
            novo_estoque = estoque_atual - qtd
            produto["estoque"] = novo_estoque  # Atualiza no dicionário

            # Aviso se o estoque estiver no limite mínimo
            if novo_estoque <= estoque_minimo:
                print(f"⚠ Produto {produto['nome']} está no limite de estoque mínimo! Reposição necessária.")

            salvar_dados(produtos_lista)  # Agora salva corretamente sem precisar de outra função
            print(f"📦 Estoque atualizado: {produto['estoque']}")
            return True

    print("❌ Produto não encontrado.")
    return False  # Retorna False se o ID do produto não existir

# Função principal para realizar a venda
def realizarVenda():
    while True:
        try:
            idproduto = int(input("Informe o ID do produto que deseja comprar: "))
            if verificar_idproduto(idproduto):
                qtd = int(input("Informe a quantidade que deseja comprar: "))
                if verificar_estoque(idproduto, qtd):
                    print("✅ Venda realizada com sucesso!")
                    break  # Encerra o loop se a venda for concluída
        except ValueError:
            print("❌ Por favor, digite um número válido.")

# Chamar a função para iniciar o processo de venda
realizarVenda()
1