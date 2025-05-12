"""
Sistema de Gerenciamento de Dados Médicos

Interface principal que integra todos os módulos do sistema:
- Autenticação de usuários (pacientes e profissionais)
- Gerenciamento de contas
- Análise de dados médicos
- Visualização e filtragem de registros
- Geração de relatórios e datasets sintéticos
- Operações administrativas
"""
from functools import partial, reduce
from pathlib import Path
from typing import Callable, List, Tuple, Dict, Optional
import sys

# Importações relativas
from src.autenticacao.autenticacao import login, criar_conta
from src.analise.carregar_dados_saude import carregar_dados_saude
from src.analise.analisar_metricas import pipeline_analise
from src.analise.visualizar_dados import visualizar_dados
from src.analise.filtrar_dados import filtrar_registros, obter_criterios_padrao
from src.analise.adicionar_exames import adicionar_exames
from src.analise.gerador_dataset_saude import gerar_dataset_csv
from relatorios.relatorios import gerar_relatorio

# Configurações de caminhos
CAMINHO_BASE = Path(__file__).parent
CAMINHO_CONTAS = CAMINHO_BASE / "data/contas.csv"
CAMINHO_DADOS = CAMINHO_BASE / "data/pacientes"

OpcaoMenu = Tuple[Callable[[], None], str]
Usuario = Dict[str, str]

def imprimir_colorido(texto: str, cor: str = "branco") -> None:
    """Imprime texto formatado com cores ANSI no terminal.
    
    Args:
        texto: String a ser impressa
        cor: Cor desejada (vermelho, verde, amarelo, azul, roxo, ciano)
    """
    cores = {"vermelho": 31, "verde": 32, "amarelo": 33, "azul": 34, "roxo": 35, "ciano": 36}
    print(f"\033[{cores.get(cor, 37)}m{texto}\033[0m")

def criar_cabecalho(titulo: str) -> None:
    """Cria um cabeçalho visualmente destacado para menus.
    
    Args:
        titulo: Texto a ser exibido no cabeçalho
    """
    borda = "═" * (len(titulo) + 2)
    list(map(
        lambda linha: imprimir_colorido(linha, "azul"),
        [borda, f" {titulo} ", borda]
    ))

def mostrar_menu(opcoes: List[OpcaoMenu]) -> None:
    """Exibe um menu numerado com as opções disponíveis.
    
    Args:
        opcoes: Lista de tuplas contendo (função, descrição) para cada opção
    """
    list(map(
        lambda i_op: imprimir_colorido(f"{i_op[0]}. {i_op[1][1]}", "ciano"),
        enumerate(opcoes, 1)
    ))

def processar_escolha(opcoes: List[OpcaoMenu], retorno: Callable) -> None:
    """Processa a seleção do usuário e executa a função correspondente.
    
    Args:
        opcoes: Lista de opções disponíveis
        retorno: Função para retornar em caso de erro
    """
    try:
        escolha = int(input("\n➤ Selecione: ")) - 1
        opcoes[escolha][0]()
    except (ValueError, IndexError):
        imprimir_colorido("Opção inválida!", "vermelho")
        retorno()

def menu_principal() -> None:
    """Exibe o menu inicial do sistema com opções básicas."""
    criar_cabecalho("Sistema de Dados Médicos")
    opcoes = [
        (menu_criar_conta, "Criar conta"),
        (menu_login, "Login"),
        (menu_administrador, "Acesso Administrativo"),
        (sair, "Sair")
    ]
    mostrar_menu(opcoes)
    processar_escolha(opcoes, menu_principal)

def menu_paciente() -> None:
    """Menu principal para pacientes com operações específicas."""
    criar_cabecalho("Área do Paciente")
    opcoes = [
        (partial(adicionar_exames), "Adicionar exames"),
        (partial(visualizar_dados_paciente), "Visualizar meus dados"),
        (partial(carregar_dados_paciente), "Carregar dados de saúde"),
        (menu_principal, "Voltar")
    ]
    mostrar_menu(opcoes)
    processar_escolha(opcoes, menu_paciente)

def menu_profissional() -> None:
    """Menu completo para profissionais de saúde com ferramentas avançadas."""
    criar_cabecalho("Área Médica")
    opcoes = [
        (partial(analisar_dados), "Analisar métricas"),
        (partial(visualizar_dados_profissional), "Visualizar dados"),
        (partial(filtrar_dados_anormais), "Filtrar dados anormais"),
        (partial(gerar_relatorio_completo), "Gerar relatório"),
        (partial(gerar_dataset_sintetico), "Gerar dataset sintético"),
        (menu_principal, "Voltar")
    ]
    mostrar_menu(opcoes)
    processar_escolha(opcoes, menu_profissional)

def menu_administrador() -> None:
    """Menu de administração com ferramentas de gerenciamento de contas."""
    criar_cabecalho("Painel Administrativo")
    opcoes = [
        (partial(criar_conta_admin), "Criar conta manual"),
        (partial(editar_conta_admin), "Editar conta"),
        (partial(excluir_conta_admin), "Excluir conta"),
        (partial(buscar_conta_admin), "Buscar conta"),
        (menu_principal, "Voltar")
    ]
    mostrar_menu(opcoes)
    processar_escolha(opcoes, menu_administrador)

def visualizar_dados_paciente() -> None:
    """Interface para visualização limitada de dados do paciente."""
    criar_cabecalho("Meus Dados de Saúde")
    caminho = buscar_arquivo("Caminho do seu arquivo CSV: ")
    visualizar_dados(caminho, 10) if caminho else menu_paciente()

def carregar_dados_paciente() -> None:
    """Carrega arquivos de dados médicos do paciente."""
    criar_cabecalho("Carregar Meus Dados")
    caminho = buscar_arquivo("Caminho do arquivo CSV: ")
    imprimir_colorido("Dados carregados com sucesso!", "verde") if caminho else None
    menu_paciente()

def analisar_dados() -> None:
    """Executa análise estatística sobre os dados médicos."""
    criar_cabecalho("Análise de Métricas")
    caminho = buscar_arquivo("Caminho do arquivo do paciente: ")
    if caminho:
        metricas = pipeline_analise(list(carregar_dados_saude(caminho)))
        list(map(
            lambda m: imprimir_colorido(f"{m[0]}: {m[1]:.2f}", "verde"),
            metricas.items()
        ))
    menu_profissional()

def visualizar_dados_profissional() -> None:
    """Visualização avançada para profissionais com controle de quantidade."""
    criar_cabecalho("Visualização Médica")
    caminho = buscar_arquivo("Caminho do arquivo CSV: ")
    qtd = input("Quantidade de registros: ").strip()
    if caminho:
        visualizar_dados(caminho, int(qtd) if qtd.isdigit() else 10)
    menu_profissional()

def filtrar_dados_anormais() -> None:
    """Identifica e exibe registros com valores fora dos parâmetros normais."""
    criar_cabecalho("Filtrar Dados Anormais")
    caminho = buscar_arquivo("Caminho do arquivo CSV: ")
    if caminho:
        resultados = filtrar_registros(
            list(carregar_dados_saude(caminho)),
            obter_criterios_padrao()
        )
        list(map(
            lambda r: imprimir_colorido(f"{r[0]}: {len(r[1])} registros", "amarelo"),
            resultados.items()
        ))
    menu_profissional()

def gerar_relatorio_completo() -> None:
    """Gera relatórios detalhados em formatos CSV ou JSON."""
    criar_cabecalho("Gerar Relatório")
    caminho = buscar_arquivo("Caminho do arquivo CSV: ")
    formato = input("Formato (csv/json): ").lower().strip()
    if caminho and formato in ['csv', 'json']:
        relatorio = gerar_relatorio(
            dados=list(carregar_dados_saude(caminho)),
            formato=formato
        )
        imprimir_colorido(f"Relatório gerado: {relatorio}", "verde")
    menu_profissional()

def gerar_dataset_sintetico() -> None:
    """Cria conjuntos de dados sintéticos para testes."""
    criar_cabecalho("Gerar Dataset Sintético")
    try:
        linhas = int(input("Número de registros: ").strip())
        caminho = gerar_dataset_csv(numero_linhas=linhas)
        imprimir_colorido(f"Dataset gerado em: {caminho}", "verde")
    except ValueError:
        imprimir_colorido("Valor inválido!", "vermelho")
    menu_profissional()

def criar_conta_admin() -> None:
    """Cria novas contas com privilégios administrativos."""
    criar_cabecalho("Criar Conta (Admin)")
    campos = ["Nome", "Email", "Senha", "Tipo (paciente/profissional)"]
    dados = list(map(lambda c: input(f"{c}: ").strip(), campos))
    email = dados[1] if dados[3] != "profissional" else f"{dados[1].split('@')[0]}@medico.com"
    sucesso, msg = criar_conta(CAMINHO_CONTAS, dados[0], email, dados[2])
    imprimir_colorido(msg, "verde" if sucesso else "vermelho")
    menu_administrador()

def editar_conta_admin() -> None:
    """Modifica informações de contas existentes."""
    criar_cabecalho("Editar Conta")
    id_conta = input("ID da conta: ").strip()
    campos = ["Novo nome (ENTER para manter)", "Novo email", "Nova senha"]
    dados = list(map(lambda c: input(f"{c}: ").strip(), campos))
    sucesso, msg = editar_conta(
        CAMINHO_CONTAS,
        id_conta,
        dados[0] or None,
        dados[1] or None,
        dados[2] or None
    )
    imprimir_colorido(msg, "verde" if sucesso else "vermelho")
    menu_administrador()

def excluir_conta_admin() -> None:
    """Remove contas do sistema de forma segura."""
    criar_cabecalho("Excluir Conta")
    id_conta = input("ID da conta: ").strip()
    sucesso, msg = excluir_conta(CAMINHO_CONTAS, id_conta)
    imprimir_colorido(msg, "verde" if sucesso else "vermelho")
    menu_administrador()

def buscar_conta_admin() -> None:
    """Localiza e exibe detalhes de contas específicas."""
    criar_cabecalho("Buscar Conta")
    id_conta = input("ID da conta: ").strip()
    conta = buscar_conta_por_id(CAMINHO_CONTAS, id_conta)
    if conta:
        list(map(
            lambda c: imprimir_colorido(f"{c[0]}: {c[1]}", "ciano"),
            conta.items()
        ))
    else:
        imprimir_colorido("Conta não encontrada!", "vermelho")
    menu_administrador()

def buscar_arquivo(mensagem: str) -> Optional[Path]:
    """Localiza arquivos no sistema de forma segura.
    
    Args:
        mensagem: Prompt a ser exibido para o usuário
    
    Returns:
        Path: Objeto Path do arquivo encontrado ou None
    """
    caminho = CAMINHO_DADOS / input(mensagem).strip()
    return caminho if caminho.exists() else (
        imprimir_colorido("Arquivo não encontrado!", "vermelho"),
        None
    )[1]

def menu_criar_conta() -> None:
    """Gerencia o fluxo de criação de novas contas de usuário."""
    criar_cabecalho("Criar Conta")
    campos = ["Nome", "Email", "Senha (mínimo 8 caracteres)"]
    dados = list(map(lambda c: input(f"{c}: ").strip(), campos))
    sucesso, msg = criar_conta(CAMINHO_CONTAS, *dados)
    imprimir_colorido(msg, "verde" if sucesso else "vermelho")
    menu_principal()

def menu_login() -> None:
    """Controla o processo de autenticação no sistema."""
    criar_cabecalho("Login")
    credenciais = list(map(
        lambda p: input(f"{p}: ").strip(),
        ["Email", "Senha"]
    ))
    sucesso, msg = login(CAMINHO_CONTAS, *credenciais)
    imprimir_colorido(msg, "verde" if sucesso else "vermelho")
    (menu_profissional if "@medico.com" in credenciais[0] else menu_paciente)() if sucesso else menu_principal()

def sair() -> None:
    """Encerra a aplicação de forma controlada."""
    imprimir_colorido("Sistema encerrado com sucesso!", "verde")
    sys.exit(0)

if __name__ == "__main__":
    CAMINHO_DADOS.mkdir(parents=True, exist_ok=True)
    if not CAMINHO_CONTAS.exists():
        CAMINHO_CONTAS.parent.mkdir(parents=True, exist_ok=True)
        CAMINHO_CONTAS.touch()
    menu_principal()