from src.utils.LLM import LLM

def interactive_llm():
    """Interface de linha de comando para interagir com a LLM"""
    while True:
        print("\nMenu de Interação com LLM:")
        print("1 - Digitar mensagem para obter resposta da IA")
        print("0 - Sair")
        
        opt = input("Opção: ")
        
        if opt == "1":
            content = input("Digite o conteúdo da mensagem:\n")
            LLM(content)
        elif opt == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    """
    Executa a interface interativa de linha de comando para a LLM
    quando o script é executado diretamente.
    """
    interactive_llm()