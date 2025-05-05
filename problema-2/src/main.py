from typing import Callable, List, Tuple
from src.autenticacao.autenticacao import login
from src.administracao.gerenciarConta import criar_conta, editar_conta, excluir_conta, buscar_conta_por_id
from src.analise.analisar_metricas import pipeline_analise
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

def executar_menu(opcoes: List[Tuple[Callable[[], None], str]], entrada: str, repetir: Callable = None) -> None:
    try:
        opcoes[int(entrada) - 1][0]()
    except (IndexError, ValueError):
        print_terminal("Opção inválida!", "vermelho")
        if repetir:
            repetir()

def menu_principal() -> None:
    cabecalho("Sistema de Dados Médicos")
    opcoes = [
        (menu_criar_conta, "Novo usuário"),
        (menu_login, "Acessar sistema"),
        (menu_administrador, "Gerenciar contas"),
        (menu_profissional, "Gerenciar dados"),
        (sair, "Encerrar programa")
    ]
    mostrar_opcoes(opcoes)
    executar_menu(opcoes, input("\nSelecione uma opção: ").strip(), menu_principal)

def sair() -> None:
    print_terminal("Até logo!", "verde")

def menu_criar_conta() -> None:
    """Fluxo de criação de conta para usuários."""
    cabecalho("Criar Conta")
    nome, email, senha = map(lambda m: input(m).strip(), ["Nome: ", "Email: ", "Senha: "])
    sucesso, msg = criar_conta("contas.csv", nome, email, senha)
    print_terminal(msg, "verde" if sucesso else "vermelho")
    menu_principal()

def menu_login() -> None:
    """Fluxo de login de usuários."""
    cabecalho("Login")
    email = input("Email: ").strip()
    senha = input("Senha: ").strip()
    sucesso, msg = login("contas.csv", email, senha)
    print_terminal(msg, "verde" if sucesso else "vermelho")
    (menu_profissional if "@medico.com" in email else menu_paciente)() if sucesso else menu_principal()

def menu_profissional() -> None:
    """Menu para usuários médicos/profissionais."""
    cabecalho("Área Médica")
    opcoes = [
        (analisar_dados, "Carregar CSV"),
        (visualizar_metricas, "Estatísticas"),
        (menu_principal, "Voltar")
    ]
    mostrar_opcoes(opcoes)
    executar_menu(opcoes, input("Opção: ").strip(), menu_profissional)

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
    opcoes = [
        (criar_conta_admin_manual, "Cadastrar novo usuário"),
        (editar_conta_manual, "Alterar dados de um usuário"),
        (excluir_conta_manual, "Remover usuário"),
        (buscar_conta_manual, "Ver dados de um usuário"),
        (menu_principal, "Voltar")
    ]
    mostrar_opcoes(opcoes)
    executar_menu(opcoes, input("Opção: ").strip(), menu_administrador)

def criar_conta_admin_manual() -> None:
    """Cria uma nova conta manualmente (admin)."""
    cabecalho("Criar Conta (Admin)")
    nome, email, senha = map(lambda m: input(m).strip(), ["Nome: ", "Email: ", "Senha: "])
    sucesso, mensagem = criar_conta("contas.csv", nome, email, senha)
    print_terminal(mensagem, "verde" if sucesso else "vermelho")
    menu_administrador()

def editar_conta_manual() -> None:
    """Edita uma conta existente."""
    cabecalho("Editar Conta")
    id_alvo = input("ID da conta: ").strip()
    novo_nome = input("Novo nome (deixe vazio): ").strip() or None
    novo_email = input("Novo email (deixe vazio): ").strip() or None
    nova_senha = input("Nova senha (deixe vazio): ").strip() or None
    sucesso, mensagem = editar_conta("contas.csv", id_alvo, novo_nome, novo_email, nova_senha)
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
