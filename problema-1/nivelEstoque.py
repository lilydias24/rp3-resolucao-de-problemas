import json


ESTOQUE_FILE = "estoque2.json"

def carregar_estoque():
    """carrega os dados do estoque do arquivo json"""
    try:
        with open(ESTOQUE_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"produtos": {}}  #retorna um estoque vazio se o arquivo não existir

def salvar_estoque(estoque):
    """salva os dados no arquivo json"""
    with open(ESTOQUE_FILE, "w") as file:
        json.dump(estoque, file, indent=4)

def adicionar_produto(nome, quantidade, minimo):
    """adiciona um novo produto ao estoque"""
    estoque = carregar_estoque()
    estoque["produtos"][nome] = {"quantidade": quantidade, "minimo": minimo}
    salvar_estoque(estoque)
    print(f"Produto {nome} adicionado com sucesso!")

def atualizar_estoque(nome, quantidade):
    """atualiza a quantidade de um produto no estoque"""
    estoque = carregar_estoque()
    if nome in estoque["produtos"]:
        estoque["produtos"][nome]["quantidade"] = quantidade
        salvar_estoque(estoque)
        print(f"Quantidade de {nome} atualizada para {quantidade}.")
    else:
        print(f"Produto {nome} não encontrado.")

def verificar_estoque():
    """verifica e alerta se algum produto estiver abaixo do mínimo"""
    estoque = carregar_estoque()
    alertas = []
    
    for produto, info in estoque["produtos"].items():
        if info["quantidade"] < info["minimo"]:
            alertas.append(f"ALERTA: {produto} está abaixo do nível mínimo! ({info['quantidade']} disponíveis)")
    
    if alertas:
        print("\n".join(alertas))
    else:
        print("todos os produtos estão dentro dos níveis de segurança.")


adicionar_produto("Arroz", 6, 5)
adicionar_produto("Feijão", 7, 5)
adicionar_produto("Óleo", 8, 2)

verificar_estoque()  # na teoria tem que alertar sobre o feijao e o arroz
