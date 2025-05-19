"""
Sistema de Gerenciamento de Dados Médicos

Interface principal que integra todos os módulos do sistema:
- Autenticação de usuários (pacientes e profissionais)
- Gerenciamento de contas de pacientes
- Análise de dados médicos
- Visualização e filtragem de registros
- Geração de relatórios e datasets sintéticos

Este módulo implementa a interface principal do sistema, seguindo princípios de
programação funcional e garantindo a integração de todos os componentes.
"""
from functools import partial, reduce
from pathlib import Path
from typing import Callable, List, Tuple, Dict, Optional, Any
import sys
from itertools import starmap

def compose(*functions):
    """Compose multiple functions into a single function.
    
    Args:
        *functions: Functions to compose, in order of application
        
    Returns:
        Callable: A function that applies all functions in sequence
        
    Example:
        >>> def add_one(x): return x + 1
        >>> def double(x): return x * 2
        >>> f = compose(add_one, double)
        >>> f(3)  # (3 + 1) * 2 = 8
        8
    """
    return reduce(lambda f, g: lambda x: f(g(x)), functions)

# Importações relativas
from .autenticacao.autenticacao import login, criar_conta
from .administracao.gerenciarConta import buscar_conta_por_id, editar_conta, excluir_conta
from .analise.carregar_dados_saude import carregar_dados_saude
from .analise.analisar_metricas import pipeline_analise
from .analise.visualizar_dados import visualizar_dados
from .analise.filtrar_dados import filtrar_registros, obter_criterios_padrao
from .analise.adicionar_exames import adicionar_exames
from .analise.gerador_dataset_saude import gerar_dataset_csv
from relatorios.relatorios import gerar_relatorio

# Configurações de caminhos
CAMINHO_BASE = Path(__file__).parent.parent
CAMINHO_CONTAS = CAMINHO_BASE / "dados/contas.csv"
CAMINHO_DADOS = CAMINHO_BASE / "dados/dados_pacientes"

# Tipos
OpcaoMenu = Tuple[Callable[[], None], str]
Usuario = Dict[str, str]
Resultado = Tuple[bool, str]

def imprimir_colorido(texto: str, cor: str = "branco") -> None:
    """Imprime texto formatado com cores ANSI no terminal.
    
    Esta função utiliza códigos ANSI para colorir o texto no terminal,
    melhorando a experiência visual do usuário.
    
    Args:
        texto (str): O texto a ser impresso no terminal.
        cor (str, optional): A cor desejada para o texto. Opções disponíveis:
            - "vermelho"
            - "verde"
            - "amarelo"
            - "azul"
            - "roxo"
            - "ciano"
            - "branco" (padrão)
    
    Returns:
        None: A função apenas imprime o texto colorido.
    """
    cores = {"vermelho": 31, "verde": 32, "amarelo": 33, "azul": 34, "roxo": 35, "ciano": 36}
    print(f"\033[{cores.get(cor, 37)}m{texto}\033[0m")

def criar_cabecalho(titulo: str) -> None:
    """Cria um cabeçalho visualmente destacado para menus.
    
    Esta função cria um cabeçalho formatado com bordas e cores para
    melhorar a organização visual dos menus do sistema.
    
    Args:
        titulo (str): O texto a ser exibido no cabeçalho.
    
    Returns:
        None: A função apenas imprime o cabeçalho formatado.
    
    Example:
        >>> criar_cabecalho("Menu Principal")
        ═══════════════
         Menu Principal 
        ═══════════════
    """
    borda = "═" * (len(titulo) + 2)
    list(map(
        lambda linha: imprimir_colorido(linha, "azul"),
        [borda, f" {titulo} ", borda]
    ))

def mostrar_menu(opcoes: List[OpcaoMenu]) -> None:
    """Exibe um menu numerado com as opções disponíveis.
    
    Esta função formata e exibe as opções do menu de forma numerada,
    utilizando cores para melhorar a legibilidade.
    
    Args:
        opcoes (List[OpcaoMenu]): Lista de tuplas contendo (função, descrição)
            para cada opção do menu.
    
    Returns:
        None: A função apenas exibe o menu formatado.
    
    Example:
        >>> opcoes = [(funcao1, "Opção 1"), (funcao2, "Opção 2")]
        >>> mostrar_menu(opcoes)
        1. Opção 1
        2. Opção 2
    """
    list(map(
        lambda i_op: imprimir_colorido(f"{i_op[0]}. {i_op[1][1]}", "ciano"),
        enumerate(opcoes, 1)
    ))

def processar_escolha(opcoes: List[OpcaoMenu], retorno: Callable) -> None:
    """Processa a seleção do usuário e executa a função correspondente.
    
    Esta função lida com a entrada do usuário, valida a escolha e
    executa a função correspondente à opção selecionada.
    
    Args:
        opcoes (List[OpcaoMenu]): Lista de opções disponíveis no menu.
        retorno (Callable): Função a ser chamada em caso de erro na seleção.
    
    Returns:
        None: A função executa a opção selecionada ou retorna ao menu anterior.
    
    Raises:
        ValueError: Se a entrada não for um número válido.
        IndexError: Se o número selecionado estiver fora do intervalo válido.
    """
    try:
        escolha = int(input("\n➤ Selecione: ")) - 1
        opcoes[escolha][0]()
    except (ValueError, IndexError):
        imprimir_colorido("Opção inválida!", "vermelho")
        retorno()

def buscar_arquivo(mensagem: str) -> Optional[Path]:
    """Busca um arquivo de forma segura.
    
    Esta função solicita ao usuário o caminho de um arquivo e verifica
    se ele existe antes de retorná-lo.
    
    Args:
        mensagem (str): A mensagem a ser exibida ao solicitar o caminho do arquivo.
    
    Returns:
        Optional[Path]: O caminho do arquivo se ele existir, None caso contrário.
    
    Example:
        >>> caminho = buscar_arquivo("Digite o caminho do arquivo: ")
        Digite o caminho do arquivo: dados.csv
        >>> print(caminho)
        PosixPath('dados.csv')
    """
    caminho = input(mensagem).strip()
    return Path(caminho) if caminho and Path(caminho).exists() else None

def menu_principal() -> None:
    """Exibe o menu inicial do sistema.
    
    Este é o ponto de entrada principal do sistema, oferecendo opções para:
    - Criar uma nova conta
    - Realizar login
    - Sair do sistema
    
    Returns:
        None: A função gerencia a navegação entre os diferentes menus.
    """
    criar_cabecalho("Sistema de Dados Médicos")
    opcoes = [
        (menu_criar_conta, "Criar conta"),
        (menu_login, "Login"),
        (sair, "Sair")
    ]
    mostrar_menu(opcoes)
    processar_escolha(opcoes, menu_principal)

def menu_paciente() -> None:
    """Menu principal para pacientes.
    
    Oferece funcionalidades específicas para pacientes:
    - Adicionar novos exames
    - Visualizar dados pessoais
    - Carregar dados de saúde
    - Gerenciar conta
    
    Returns:
        None: A função gerencia a navegação entre as opções do paciente.
    """
    criar_cabecalho("Área do Paciente")
    opcoes = [
        (partial(adicionar_exames), "Adicionar exames"),
        (partial(visualizar_dados_paciente), "Visualizar meus dados"),
        (partial(carregar_dados_paciente), "Carregar dados de saúde"),
        (partial(menu_gerenciar_conta), "Gerenciar minha conta"),
        (menu_principal, "Voltar")
    ]
    mostrar_menu(opcoes)
    processar_escolha(opcoes, menu_paciente)

def menu_profissional() -> None:
    """Menu para profissionais de saúde.
    
    Oferece funcionalidades avançadas para profissionais:
    - Análise de métricas
    - Visualização detalhada de dados
    - Filtragem de dados anormais
    - Geração de relatórios
    - Criação de datasets sintéticos
    
    Returns:
        None: A função gerencia a navegação entre as opções do profissional.
    """
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

def visualizar_dados_paciente() -> None:
    """Interface para visualização de dados do paciente.
    
    Permite ao paciente visualizar seus próprios dados de saúde,
    com uma visualização limitada a 10 registros por vez.
    
    Returns:
        None: A função exibe os dados e retorna ao menu do paciente.
    """
    criar_cabecalho("Meus Dados de Saúde")
    caminho = buscar_arquivo("Caminho do seu arquivo CSV: ")
    if caminho:
        compose(
            lambda _: menu_paciente(),
            lambda dados: visualizar_dados(dados, 10),
            carregar_dados_saude
        )(caminho)
    else:
        menu_paciente()

def carregar_dados_paciente() -> None:
    """Carrega arquivos de dados médicos do paciente.
    
    Permite ao paciente carregar seus dados de saúde a partir
    de um arquivo CSV.
    
    Returns:
        None: A função carrega os dados e retorna ao menu do paciente.
    """
    criar_cabecalho("Carregar Meus Dados")
    caminho = buscar_arquivo("Caminho do arquivo CSV: ")
    if caminho:
        compose(
            lambda _: imprimir_colorido("Dados carregados com sucesso!", "verde"),
            lambda _: menu_paciente(),
            carregar_dados_saude
        )(caminho)
    else:
        menu_paciente()

def analisar_dados() -> None:
    """Executa análise estatística sobre os dados médicos.
    
    Calcula métricas estatísticas como média, mediana, moda,
    desvio padrão e variância sobre os dados do paciente.
    
    Returns:
        None: A função exibe as métricas calculadas e retorna ao menu do profissional.
    """
    criar_cabecalho("Análise de Métricas")
    caminho = buscar_arquivo("Caminho do arquivo do paciente: ")
    if caminho:
        compose(
            lambda _: menu_profissional(),
            lambda metricas: list(starmap(
                lambda k, v: imprimir_colorido(f"{k}: {v:.2f}", "verde"),
                metricas.items()
            )),
            pipeline_analise,
            carregar_dados_saude
        )(caminho)
    else:
        menu_profissional()

def visualizar_dados_profissional() -> None:
    """Visualização avançada para profissionais.
    
    Permite ao profissional visualizar dados dos pacientes com
    controle sobre a quantidade de registros exibidos.
    
    Returns:
        None: A função exibe os dados e retorna ao menu do profissional.
    """
    criar_cabecalho("Visualização Médica")
    caminho = buscar_arquivo("Caminho do arquivo CSV: ")
    qtd = input("Quantidade de registros: ").strip()
    if caminho:
        compose(
            lambda _: menu_profissional(),
            lambda dados: visualizar_dados(dados, int(qtd) if qtd.isdigit() else 10),
            carregar_dados_saude
        )(caminho)
    else:
        menu_profissional()

def filtrar_dados_anormais() -> None:
    """Identifica registros com valores fora dos parâmetros normais.
    
    Analisa os dados do paciente e identifica registros que
    apresentam valores fora dos parâmetros considerados normais.
    
    Returns:
        None: A função exibe os registros anormais e retorna ao menu do profissional.
    """
    criar_cabecalho("Filtrar Dados Anormais")
    caminho = buscar_arquivo("Caminho do arquivo CSV: ")
    if caminho:
        compose(
            lambda _: menu_profissional(),
            lambda resultados: list(starmap(
                lambda k, v: imprimir_colorido(f"{k}: {len(v)} registros", "amarelo"),
                resultados.items()
            )),
            lambda dados: filtrar_registros(dados, obter_criterios_padrao()),
            carregar_dados_saude
        )(caminho)
    else:
        menu_profissional()

def gerar_relatorio_completo() -> None:
    """Gera relatórios detalhados.
    
    Cria relatórios detalhados dos dados do paciente em formatos
    CSV ou JSON, incluindo análises e métricas.
    
    Returns:
        None: A função gera o relatório e retorna ao menu do profissional.
    """
    criar_cabecalho("Gerar Relatório")
    caminho = buscar_arquivo("Caminho do arquivo CSV: ")
    formato = input("Formato (csv/json): ").lower().strip()
    if caminho and formato in ['csv', 'json']:
        compose(
            lambda _: menu_profissional(),
            lambda relatorio: imprimir_colorido(f"Relatório gerado: {relatorio}", "verde"),
            lambda dados: gerar_relatorio(dados, formato),
            carregar_dados_saude
        )(caminho)
    else:
        menu_profissional()

def gerar_dataset_sintetico() -> None:
    """Cria conjuntos de dados sintéticos.
    
    Gera datasets sintéticos para testes e desenvolvimento,
    com dados que simulam registros médicos reais.
    
    Returns:
        None: A função gera o dataset e retorna ao menu do profissional.
    
    Raises:
        ValueError: Se o número de registros não for um valor válido.
    """
    criar_cabecalho("Gerar Dataset Sintético")
    try:
        linhas = int(input("Número de registros: ").strip())
        compose(
            lambda _: menu_profissional(),
            lambda caminho: imprimir_colorido(f"Dataset gerado em: {caminho}", "verde"),
            gerar_dataset_csv
        )(linhas)
    except ValueError:
        imprimir_colorido("Valor inválido!", "vermelho")
        menu_profissional()

def menu_criar_conta() -> None:
    """Interface para criação de conta.
    
    Permite ao usuário criar uma nova conta no sistema.
    O tipo de usuário é determinado pelo email:
    - @medico.com: profissional
    - outros: paciente
    
    Returns:
        None: A função cria a conta e retorna ao menu principal.
    """
    criar_cabecalho("Criar Conta")
    
    # Solicita nome e email
    nome = input("Nome: ").strip()
    email = input("Email: ").strip()
    
    # Mostra requisitos da senha
    imprimir_colorido("\nRequisitos da senha:", "amarelo")
    imprimir_colorido("- Pelo menos 8 caracteres", "amarelo")
    imprimir_colorido("- Pelo menos uma letra maiúscula", "amarelo")
    imprimir_colorido("- Pelo menos uma letra minúscula", "amarelo")
    imprimir_colorido("- Pelo menos um número", "amarelo")
    print()  # Linha em branco para separar
    
    # Solicita a senha
    senha = input("Senha: ").strip()
    
    # Cria a conta
    compose(
        lambda _: menu_principal(),
        lambda msg: imprimir_colorido(msg[1], "verde" if msg[0] else "vermelho"),
        lambda dados: criar_conta(CAMINHO_CONTAS, dados[0], dados[1], dados[2])
    )((nome, email, senha))

def menu_login() -> None:
    """Interface para login.
    
    Permite ao usuário realizar login no sistema,
    redirecionando para o menu apropriado após autenticação.
    O tipo de usuário é determinado pelo email:
    - @medico.com: profissional
    - outros: paciente
    
    Returns:
        None: A função autentica o usuário e redireciona para o menu apropriado.
    """
    criar_cabecalho("Login")
    email = input("Email: ").strip()
    senha = input("Senha: ").strip()
    compose(
        lambda resultado: (
            menu_profissional() if "@medico.com" in resultado[1]["email"] else menu_paciente()
        ) if resultado[0] else menu_principal(),
        lambda credenciais: login(CAMINHO_CONTAS, credenciais[0], credenciais[1])
    )((email, senha))

def sair() -> None:
    """Encerra o programa.
    
    Finaliza a execução do sistema de forma segura.
    
    Returns:
        None: A função encerra o programa.
    """
    sys.exit(0)

def menu_gerenciar_conta() -> None:
    """Menu de gerenciamento de conta do paciente."""
    criar_cabecalho("Gerenciar Minha Conta")
    
    def visualizar():
        criar_cabecalho("Meus Dados Cadastrais")
        email = input("Email: ").strip()
        conta = buscar_conta_por_id(CAMINHO_CONTAS, email)
        if conta:
            list(starmap(
                lambda k, v: imprimir_colorido(f"{k}: {v}", "ciano"),
                conta.items()
            ))
        menu_gerenciar_conta()
    
    def editar():
        criar_cabecalho("Editar Meus Dados")
        email = input("Email atual: ").strip()
        campos = ["Novo nome (ENTER para manter)", "Novo email", "Nova senha"]
        dados = list(map(lambda c: input(f"{c}: ").strip(), campos))
        resultado = editar_conta(
            CAMINHO_CONTAS,
            email,
            dados[0] or None,
            dados[1] or None,
            dados[2] or None
        )
        imprimir_colorido(resultado[1], "verde" if resultado[0] else "vermelho")
        menu_gerenciar_conta()
    
    def excluir():
        criar_cabecalho("Excluir Minha Conta")
        email = input("Email: ").strip()
        senha = input("Senha (para confirmar): ").strip()
        resultado = excluir_conta(CAMINHO_CONTAS, email)
        imprimir_colorido(resultado[1], "verde" if resultado[0] else "vermelho")
        menu_principal()
    
    opcoes = [
        (visualizar, "Visualizar meus dados"),
        (editar, "Editar informações"),
        (excluir, "Excluir minha conta"),
        (menu_paciente, "Voltar")
    ]
    mostrar_menu(opcoes)
    processar_escolha(opcoes, menu_gerenciar_conta)

if __name__ == "__main__":
    menu_principal()