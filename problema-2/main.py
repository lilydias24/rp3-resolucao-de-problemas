from autenticacao import criar_conta, login, salvar_contas
from typing import List, Dict

CAMINHO_CSV = "contas.csv"

def exibir_menu():
    """exibe o menu principal."""
    while True:
        print("\n=== Sistema de Usuários ===")
        print("1. Criar conta")
        print("2. Fazer login")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Digite seu nome: ").strip()
            email = input("Digite seu email: ").strip()
            senha = input("Digite sua senha: ").strip()
            sucesso, mensagem, novas_contas = criar_conta(CAMINHO_CSV, nome, email, senha)
            if sucesso:
                salvar_contas(CAMINHO_CSV, novas_contas)
            print(mensagem)

        elif opcao == "2":
            email = input("Digite seu email: ").strip()
            senha = input("Digite sua senha: ").strip()
            sucesso, mensagem = login(CAMINHO_CSV, email, senha)
            print(mensagem)

        elif opcao == "3":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    exibir_menu()