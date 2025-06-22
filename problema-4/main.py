from utils.LLM import LLM

while True:
    print("Teste do uso da LLM com Groq, Escolha uma opção: ")
    print("1 - Digitar mensagem para obter resposta da IA")
    print("0 - Sair")
    
    opt = input()
    if opt == "1":
        print("Digite o conteúdo da mensagem:")
        LLM(content = input())
    if opt == "0":
        print("Saindo...")
        break