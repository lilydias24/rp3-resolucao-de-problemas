from aspects.LLM import generate_epics_with_llm
from utils.epics import print_epics

def pedir_product_info():
    """Coleta informações do produto via CLI"""
    print("\n" + "="*50)
    print("GERADOR DE ÉPICOS - MODO CLI")
    print("="*50)
    
    nome = input("Nome do produto: ")
    descricao = input("Descrição do produto: ")
    personas = input("Personas (separe por vírgula): ").split(",")
    personas = [p.strip() for p in personas]
    proposta_valor = input("Proposta de valor: ")
    canais = input("Canais/Plataformas (opcional): ")
    
    return {
        "nome": nome,
        "descricao": descricao,
        "personas": personas,
        "proposta_valor": proposta_valor,
        "canais": canais
    }

def main():
    """Função principal do modo CLI"""
    while True:
        print("\n" + "="*50)
        print("Bem vindo PO! Escolha uma opção:")
        print("1 - Gerar épicos para um produto (usando LLM)")
        print("2 - Gerar épicos com prompt customizado")
        print("0 - Sair")
        print("="*50)
        
        opt = input("Opção: ")
        
        if opt == "1":
            product_info = pedir_product_info()
            print("\nGerando épicos...")
            epics = generate_epics_with_llm(product_info)
            print_epics(epics)
            
        elif opt == "2":
            product_info = pedir_product_info()
            custom_prompt = input("\nPrompt customizado (deixe vazio para usar padrão): ")
            
            if custom_prompt.strip():
                # aqui vai o prompt customizado, quando eu fizer
                print("Funcionalidade de prompt customizado vai ser implementada em breve")
            else:
                print("\nGerando épicos com prompt padrão...")
                epics = generate_epics_with_llm(product_info)
                print_epics(epics)
                
        elif opt == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()