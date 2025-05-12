import csv
from typing import Callable, List, Tuple, Dict
from src.autenticacao.autenticacao import login
from src.administracao.gerenciarConta import criar_conta, editar_conta, excluir_conta, buscar_conta_por_id
from src.analise.analisar_metricas import pipeline_analise
from src.analise.visualizar_dados import visualizar_dados
from src.analise.filtrar_dados import filtrar_registros, obter_criterios_padrao
from src.analise.adicionar_exames import adicionar_exames
from src.analise.gerador_dataset_saude import gerar_dataset_csv
from functools import partial, reduce
import os

# Funções auxiliares (puras)
def print_terminal(mensagem: str, cor: str = "branco", estilo: str = "normal") -> None:
    cores = {
        "preto": 30, "vermelho": 31, "verde": 32, "amarelo": 33,
        "azul": 34, "roxo": 35, "ciano": 36, "branco": 37
    }
    estilos = {"normal": 0, "negrito": 1, "sublinhado": 4}
    codigo = lambda c, e: f"\033[{estilos.get(e, 0)};{cores.get(c, 37)}m"
    print(f"{codigo(cor, estilo)}{mensagem}\033[0m")

def cabecalho(titulo: str) -> None:
    print_terminal("\n" + "~" * 50, "azul", "negrito")
    print_terminal(f"{titulo:^50}", "azul", "negrito")
    print_terminal("~" * 50, "azul", "negrito")

def mostrar_opcoes(opcoes: List[Tuple[Callable[[], None], str]]) -> None:
    """Lista as opções disponíveis no menu."""
    
    descricoes = list(map(lambda op: op[1], opcoes))
    
    list(map(
        lambda item: print_terminal(f"{item[0]}. {item[1]}", "ciano"),
        enumerate(descricoes, 1)
    ))

def executar_menu(opcoes: List[Tuple[Callable[[], None], str]], entrada: str, repetir: Callable = None) -> None:
    try:
        opcoes[int(entrada) - 1][0]()
    except (IndexError, ValueError):
        print_terminal("Opção inválida!", "vermelho")
        repetir and repetir()

# Fluxo principal
def menu_principal() -> None:
    cabecalho("Sistema de Dados Médicos")
    opcoes = [
        (menu_criar_conta, "Criar nova conta"),
        (menu_login, "Login"),
        (menu_administrador, "Painel Administrativo"),
        (sair, "Sair do sistema")
    ]
    mostrar_opcoes(opcoes)
    executar_menu(opcoes, input("\nSelecione uma opção: ").strip(), menu_principal)

def sair() -> None:
    print_terminal("Até logo!", "verde")
    exit()

# Autenticação
def menu_criar_conta() -> None:
    cabecalho("Criar Conta")
    dados = list(map(lambda m: input(m).strip(), ["Nome completo: ", "Email: ", "Senha (mínimo 8 caracteres): "]))
    sucesso, msg = criar_conta("contas.csv", *dados)
    print_terminal(msg, "verde" if sucesso else "vermelho")
    menu_principal()

def menu_login() -> None:
    cabecalho("Login")
    email, senha = map(lambda m: input(m).strip(), ["Email: ", "Senha: "])
    sucesso, msg = login("contas.csv", email, senha)
    
    print_terminal(msg, "verde" if sucesso else "vermelho")
    (menu_profissional if "@medico.com" in email else menu_paciente)() if sucesso else menu_principal()

# Área do Paciente
def menu_paciente() -> None:
    cabecalho("Área do Paciente")
    opcoes = [
        (adicionar_exames, "Adicionar novos exames"),
        (carregar_dados_paciente, "Carregar dados de saúde (CSV)"),
        (visualizar_dados_paciente, "Visualizar meus dados"),
        (menu_principal, "Voltar")
    ]
    mostrar_opcoes([(func, desc) for func, desc in opcoes])
    executar_menu(opcoes, input("\nSelecione uma opção: ").strip(), menu_paciente)

def carregar_dados_paciente() -> None:
    cabecalho("Carregar Meus Dados")
    caminho = input("Caminho do arquivo CSV: ").strip()
    print_terminal("Dados carregados com sucesso!" if os.path.exists(caminho) else "Arquivo não encontrado!", 
                  "verde" if os.path.exists(caminho) else "vermelho")
    menu_paciente()

def visualizar_dados_paciente() -> None:
    cabecalho("Meus Dados de Saúde")
    caminho = input("Caminho do arquivo CSV: ").strip()
    os.path.exists(caminho) and visualizar_dados(caminho, 10)
    menu_paciente()

# Área Profissional
def menu_profissional() -> None:
    cabecalho("Área Médica")
    opcoes = [
        (carregar_dados_profissional, "Carregar dados de paciente"),
        (analisar_dados, "Analisar métricas"),
        (visualizar_dados_profissional, "Visualizar dados"),
        (menu_filtrar_dados, "Filtrar dados anormais"),
        (menu_gerar_dataset, "Gerar dataset sintético"),
        (menu_principal, "Voltar")
    ]
    mostrar_opcoes([(func, desc) for func, desc in opcoes])
    executar_menu(opcoes, input("\nSelecione uma opção: ").strip(), menu_profissional)

def carregar_dados_profissional() -> None:
    cabecalho("Carregar Dados do Paciente")
    caminho = input("Caminho do arquivo CSV: ").strip()
    print_terminal("Dados carregados com sucesso!" if os.path.exists(caminho) else "Arquivo não encontrado!", 
                  "verde" if os.path.exists(caminho) else "vermelho")
    menu_profissional()

def analisar_dados() -> None:
    cabecalho("Análise de Métricas")
    caminho = input("Caminho do arquivo CSV: ").strip()
    
    def exibir_metricas(metricas: Dict[str, float]) -> None:
        print_terminal("\nResultados da Análise:", "azul", "negrito")
        list(map(
            lambda item: print_terminal(f"{item[0].capitalize()}: {item[1]:.2f}", "ciano"),
            metricas.items()
        ))
    
    try:
        metricas = pipeline_analise(caminho)
        metricas and exibir_metricas(metricas) or print_terminal("Nenhum dado válido encontrado.", "amarelo")
    except Exception as e:
        print_terminal(f"Erro na análise: {str(e)}", "vermelho")
    finally:
        menu_profissional()

def visualizar_dados_profissional() -> None:
    cabecalho("Visualizar Dados do Paciente")
    caminho = input("Caminho do arquivo CSV: ").strip()
    qtd = input("Quantidade de registros (padrão 10): ").strip()
    
    try:
        visualizar_dados(caminho, int(qtd) if qtd.isdigit() else 10)
    except Exception as e:
        print_terminal(f"Erro ao visualizar: {str(e)}", "vermelho")
    finally:
        menu_profissional()

def menu_filtrar_dados() -> None:
    cabecalho("Filtrar Dados Anormais")
    caminho = input("Caminho do arquivo CSV: ").strip()
    
    if os.path.exists(caminho):
        criterios = obter_criterios_padrao()
        resultados = filtrar_registros(carregar_dados(caminho), criterios)
        
        print_terminal("\nRegistros fora do padrão:", "azul", "negrito")
        list(map(
            lambda item: print_terminal(f"{item[0]}: {len(item[1])} registros", "amarelo"),
            resultados.items()
        ))
    else:
        print_terminal("Arquivo não encontrado!", "vermelho")
    
    menu_profissional()

def menu_gerar_dataset() -> None:
    cabecalho("Gerar Dataset Sintético")
    try:
        linhas = int(input("Número de registros a gerar: ").strip())
        caminho = gerar_dataset_csv(numero_linhas=linhas)
        print_terminal(f"Dataset gerado em: {caminho}", "verde")
    except ValueError:
        print_terminal("Número inválido de registros!", "vermelho")
    finally:
        menu_profissional()

def carregar_dados(caminho: str) -> List[Dict[str, str]]:
    """Função auxiliar para carregar dados do CSV"""
    with open(caminho, "r", encoding="utf-8") as file:
        return list(csv.DictReader(file))

# Painel Administrativo
def menu_administrador() -> None:
    cabecalho("Painel Administrativo")
    opcoes = [
        (criar_conta_admin_manual, "Criar conta manualmente"),
        (editar_conta_manual, "Editar conta"),
        (excluir_conta_manual, "Excluir conta"),
        (buscar_conta_manual, "Buscar conta"),
        (menu_principal, "Voltar")
    ]
    mostrar_opcoes([(func, desc) for func, desc in opcoes])
    executar_menu(opcoes, input("\nSelecione uma opção: ").strip(), menu_administrador)

def criar_conta_admin_manual() -> None:
    cabecalho("Criar Conta (Admin)")
    nome = input("Nome completo: ").strip()
    email = input("Email: ").strip()
    senha = input("Senha: ").strip()
    tipo = input("Tipo (paciente/profissional): ").strip().lower()
    
    email = email if tipo != "profissional" else f"{email.split('@')[0]}@medico.com"
    sucesso, msg = criar_conta("contas.csv", nome, email, senha)
    
    print_terminal(msg, "verde" if sucesso else "vermelho")
    menu_administrador()

def editar_conta_manual() -> None:
    cabecalho("Editar Conta")
    id_alvo = input("ID da conta: ").strip()
    novo_nome = input("Novo nome (opcional): ").strip() or None
    novo_email = input("Novo email (opcional): ").strip() or None
    nova_senha = input("Nova senha (opcional): ").strip() or None
    
    sucesso, msg = editar_conta("contas.csv", id_alvo, novo_nome, novo_email, nova_senha)
    print_terminal(msg, "verde" if sucesso else "vermelho")
    menu_administrador()

def excluir_conta_manual() -> None:
    cabecalho("Excluir Conta")
    id_alvo = input("ID da conta: ").strip()
    sucesso, msg = excluir_conta("contas.csv", id_alvo)
    print_terminal(msg, "verde" if sucesso else "vermelho")
    menu_administrador()

def buscar_conta_manual() -> None:
    cabecalho("Buscar Conta")
    id_alvo = input("ID da conta: ").strip()
    conta = buscar_conta_por_id("contas.csv", id_alvo)
    
    if conta:
        list(map(
            lambda item: print_terminal(f"{item[0].capitalize()}: {item[1]}", "ciano"),
            conta.items()
        ))
    else:
        print_terminal("Conta não encontrada!", "vermelho")
    
    menu_administrador()

if __name__ == "__main__":
    menu_principal()