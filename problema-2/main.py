from typing import Callable, List, Tuple
from autenticacao import criar_conta as criar_conta_usuario, login
from gerenciarConta import editar_conta, excluir_conta, buscar_conta_por_id, criar_conta as criar_conta_admin
from analisar_metricas import pipeline_analise
from functools import partial
import os

def print_terminal(mensagem: str, cor: str = "branco", estilo: str = "normal") -> None:
    """Exibe mensagens coloridas no terminal."""
    cores = {
        "preto": 30, "vermelho": 31, "verde": 32, "amarelo": 33,
        "azul": 34, "roxo": 35, "ciano": 36, "branco": 37
    }
    estilos = {"normal": 0, "negrito": 1, "sublinhado": 4}
    codigo = lambda c, e: f"\033[{estilos.get(e, 0)};{cores.get(c, 37)}m"
    print(f"{codigo(cor, estilo)}{mensagem}\033[0m")

def cabecalho(titulo: str) -> None:
    """Exibe um cabeçalho estilizado."""
    print_terminal("\n" + "~" * 50, "azul", "negrito")
    print_terminal(f"{titulo:^50}", "azul", "negrito")
    print_terminal("~" * 50, "azul", "negrito")

def mostrar_opcoes(opcoes: List[Tuple[str, str]]) -> None:
    """Lista as opções disponíveis no menu."""
    list(map(
        lambda op: print_terminal(f"{op[0]}. {op[1][1]}", "ciano"),
        enumerate(opcoes, 1)
    ))

def menu_principal() -> None:
    """Menu principal do sistema."""
    cabecalho("Sistema de Dados Médicos")
    mostrar_opcoes([
        ("Criar conta", "Novo usuário"),
        ("Fazer login", "Acessar sistema"),
        ("Painel administrativo", "Gerenciar contas"),
        ("Sair", "Encerrar programa")
    ])

    (lambda escolha: (
        menu_criar_conta() if escolha == "1" else
        menu_login() if escolha == "2" else
        menu_administrador() if escolha == "3" else
        print_terminal("Até logo!", "verde") if escolha == "4" else
        (print_terminal("Opção inválida!", "vermelho"), menu_principal())
    ))(input("\n Selecione uma das opções acima : ").strip())

def menu_criar_conta() -> None:
    """Fluxo de criação de conta para usuários."""
    cabecalho("Criar Conta")
    obter_input = lambda msg: input(msg).strip()
    nome, email, senha = map(obter_input, ["Nome: ", "Email: ", "Senha: "])

    (lambda resultado: (
        print_terminal("Conta criada!", "verde"),
        menu_principal()
    ) if resultado[0] else (
        print_terminal(resultado[1], "vermelho"),
        menu_criar_conta()
    ))(criar_conta_usuario("contas.csv", nome, email, senha))

def menu_login() -> None:
    """Fluxo de login de usuários."""
    cabecalho("Login")
    email, senha = map(partial(input, "Email: "), ["", "Senha: "])

    (lambda sucesso, msg: (
        print_terminal(msg, "verde"),
        menu_profissional() if "@medico.com" in email else menu_paciente()
    ) if sucesso else (
        print_terminal(msg, "vermelho"),
        menu_principal()
    ))(*login("contas.csv", email, senha))

def menu_profissional() -> None:
    """Menu para usuários médicos/profissionais."""
    cabecalho("Área Médica")
    mostrar_opcoes([
        ("Analisar dados", "Carregar CSV"),
        ("Visualizar métricas", "Estatísticas"),
        ("Voltar", "Menu Principal")
    ])

    (lambda escolha: (
        analisar_dados() if escolha == "1" else
        visualizar_metricas() if escolha == "2" else
        menu_principal() if escolha == "3" else
        (print_terminal("Opção inválida!", "vermelho"), menu_profissional())
    ))(input("Opção: ").strip())

def menu_paciente() -> None:
    """Menu para usuários pacientes."""
    cabecalho("Área do Paciente")
    print_terminal("Bem-vindo! Navegação simples por enquanto.", "verde")
    menu_principal()

def analisar_dados() -> None:
    """Executa a análise de dados de saúde."""
    cabecalho("Análise de Dados")
    caminho = input("Caminho do CSV: ").strip()

    if not os.path.exists(caminho):
        print_terminal("Arquivo não encontrado!", "vermelho")
        return analisar_dados()

    try:
        metricas = pipeline_analise(caminho)
        for nome, valor in metricas.items():
            print_terminal(f"{nome.capitalize()}: {valor:.2f}", "ciano")
    except Exception as e:
        print_terminal(f"Erro ao analisar dados: {e}", "vermelho")
    finally:
        menu_profissional()

def visualizar_metricas() -> None:
    """Placeholder para visualização de métricas."""
    print_terminal("Funcionalidade de visualizar métricas ainda em construção!", "amarelo")
    menu_profissional()

def menu_administrador() -> None:
    """Menu para administração de contas."""
    cabecalho("Painel Administrativo")
    mostrar_opcoes([
        ("Criar conta manualmente", "Cadastrar novo usuário"),
        ("Editar conta", "Alterar dados de um usuário"),
        ("Excluir conta", "Remover usuário"),
        ("Buscar conta por ID", "Ver dados de um usuário"),
        ("Voltar", "Menu Principal")
    ])

    (lambda escolha: (
        criar_conta_admin_manual() if escolha == "1" else
        editar_conta_manual() if escolha == "2" else
        excluir_conta_manual() if escolha == "3" else
        buscar_conta_manual() if escolha == "4" else
        menu_principal() if escolha == "5" else
        (print_terminal("Opção inválida!", "vermelho"), menu_administrador())
    ))(input("Opção: ").strip())

def criar_conta_admin_manual() -> None:
    """Cria uma nova conta manualmente (admin)."""
    cabecalho("Criar Conta (Admin)")
    nome, email, senha = map(lambda msg: input(msg).strip(), ["Nome: ", "Email: ", "Senha: "])
    sucesso, mensagem = criar_conta_admin("contas.csv", nome, email, senha)
    print_terminal(mensagem, "verde" if sucesso else "vermelho")
    menu_administrador()

def editar_conta_manual() -> None:
    """Edita uma conta existente."""
    cabecalho("Editar Conta")
    id_alvo = input("ID da conta: ").strip()
    novo_nome = input("Novo nome (deixe vazio para manter): ").strip()
    novo_email = input("Novo email (deixe vazio para manter): ").strip()
    nova_senha = input("Nova senha (deixe vazio para manter): ").strip()
    sucesso, mensagem = editar_conta("contas.csv", id_alvo, novo_nome or None, novo_email or None, nova_senha or None)
    print_terminal(mensagem, "verde" if sucesso else "vermelho")
    menu_administrador()

def excluir_conta_manual() -> None:
    """Exclui uma conta existente."""
    cabecalho("Excluir Conta")
    id_alvo = input("ID da conta: ").strip()
    sucesso, mensagem = excluir_conta("contas.csv", id_alvo)
    print_terminal(mensagem, "verde" if sucesso else "vermelho")
    menu_administrador()

def buscar_conta_manual() -> None:
    """Busca uma conta pelo ID."""
    cabecalho("Buscar Conta")
    id_alvo = input("ID da conta: ").strip()
    conta = buscar_conta_por_id("contas.csv", id_alvo)
    if conta:
        print_terminal(f"ID: {conta['id']}", "ciano")
        print_terminal(f"Nome: {conta['nome']}", "ciano")
        print_terminal(f"Email: {conta['email']}", "ciano")
    else:
        print_terminal("Conta não encontrada!", "vermelho")
    menu_administrador()

if __name__ == "__main__":
    menu_principal()
