from aspects.LLM import generate_epics_with_llm
from utils.epics import print_epics

def pedir_product_info():
    nome = input("Nome do produto: ")
    descricao = input("Descrição do produto: ")
    personas = input("Personas (separe por vírgula): ").split(",")
    personas = [p.strip() for p in personas]
    proposta_valor = input("Proposta de valor: ")
    return {
        "nome": nome,
        "descricao": descricao,
        "personas": personas,
        "proposta_valor": proposta_valor
    }

while True:
    print("\nBem vindo PO! Escolha uma opção:")
    print("1 - Gerar épicos para um produto (usando LLM)")
    print("0 - Sair")
    opt = input()
    if opt == "1":
        product_info = pedir_product_info()
        epics = generate_epics_with_llm(product_info)
        print_epics(epics)
    elif opt == "0":
        print("Saindo...")
        break
    else:
        print("Opção inválida!")
