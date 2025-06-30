from aspects.LLM import *
from utils.epics import Epic
from utils.epics import print_epics

while True:
    print("Bem vindo PO!, Escolha uma opção: ")
    print("1 - Digitar mensagem para obter resposta da IA")
    print("0 - Sair")
    
    opt = input()
    if opt == "1":
        print("Digite o conteúdo da mensagem:")
        gerar_historia_usuario(content = input())
    if opt == "0":
        print("Saindo...")
        break
