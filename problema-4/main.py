from utils.LLM import LLM
from epics import Epic
from utils.LLM import generate_epics_with_llm
from epics import print_epics

product_info = {
    "nome": "Sistema de Gestão de escola",
    "descricao": "Um sistema para facilitar a gestão da escola.",
    "personas": ["professor", "aluno", "diretor"],
    "proposta_valor": "Facilitar gestão escolar."
}

while True:
    print("Teste do uso da LLM com Groq, Escolha uma opção: ")
    print("1 - Digitar mensagem para obter resposta da IA")
    print("2 - Gerar épicos para um produto (usando LLM)")
    print("0 - Sair")
    
    opt = input()
    if opt == "1":
        print("Digite o conteúdo da mensagem:")
        LLM(content = input())

    elif opt == "2":
        epics = generate_epics_with_llm(product_info)
        print_epics(epics)
    elif opt == "0":
        print("Saindo...")
        break
    else:
        print("Opção inválida!")