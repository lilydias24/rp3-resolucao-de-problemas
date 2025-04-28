from autenticacao import criar_conta, login, salvar_contas, redefinir_senha, recuperar_senha
from typing import List, Dict

CAMINHO_CSV = "contas.csv"

def ambiente_usuario(nome: str):
    """ambiente do usuário logado."""
    while True:
        print(f"\n=== Bem-vindo(a), {nome}! ===")
        print("1. Logout")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("Você fez logout com sucesso.")
            break
        else:
            print("Opção inválida. Tente novamente.")

def exibir_menu():
    """exibe o menu principal."""
    while True:
        print("\n=== Sistema de Usuários ===")
        print("1. Criar conta")
        print("2. Fazer login")
        print("3. Redefinir senha")
        print("4. Sair")
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
            if sucesso:
                # deixa o usuário logado e entra no ambiente
                nome_usuario = mensagem.split(", ")[1].replace(".", "") 
                ambiente_usuario(nome_usuario)

        elif opcao == "3":
            print("\n=== Redefinir Senha ===")
            print("1. Redefinir com senha antiga")
            print("2. Esqueceu sua senha?")
            sub_opcao = input("Escolha uma opção: ")

            if sub_opcao == "1":
                email = input("Digite seu email: ").strip()
                senha_antiga = input("Digite sua senha antiga: ").strip()
                nova_senha = input("Digite sua nova senha: ").strip()
                sucesso, mensagem, novas_contas = redefinir_senha(CAMINHO_CSV, email, senha_antiga, nova_senha)
                if sucesso:
                    salvar_contas(CAMINHO_CSV, novas_contas)
                print(mensagem)

            elif sub_opcao == "2":
                email = input("Digite seu email: ").strip()
                nova_senha = input("Digite sua nova senha: ").strip()
                sucesso, mensagem, novas_contas = recuperar_senha(CAMINHO_CSV, email, nova_senha)
                if sucesso:
                    salvar_contas(CAMINHO_CSV, novas_contas)
                print(mensagem)

            else:
                print("Opção inválida. Tente novamente.")

        elif opcao == "4":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    exibir_menu()