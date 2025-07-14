"""
Módulo para formatação de cores no terminal.
"""
from colorama import init, Fore, Back, Style

# Inicializa o colorama
init()

# Cores básicas
VERMELHO = '\033[91m'
VERDE = '\033[92m'
AMARELO = '\033[93m'
AZUL = '\033[94m'
MAGENTA = '\033[95m'
CIANO = '\033[96m'
BRANCO = '\033[97m'

# Estilos
NEGRITO = '\033[1m'
ITALICO = '\033[3m'
SUBLINHADO = '\033[4m'
INVERTIDO = '\033[7m'

# Reset
RESET = '\033[0m'

def titulo(texto: str) -> str:
    """Formata um texto como título."""
    return f"{Fore.CYAN}{Style.BRIGHT}{texto}{Style.RESET_ALL}"

def sucesso(texto: str) -> str:
    """Formata um texto como mensagem de sucesso."""
    return f"{Fore.GREEN}{texto}{Style.RESET_ALL}"

def erro(texto: str) -> str:
    """Formata um texto como mensagem de erro."""
    return f"{Fore.RED}{texto}{Style.RESET_ALL}"

def aviso(texto: str) -> str:
    """Formata um texto como aviso."""
    return f"{Fore.YELLOW}{texto}{Style.RESET_ALL}"

def destaque(texto: str) -> str:
    """Formata um texto como destaque."""
    return f"{Fore.MAGENTA}{Style.BRIGHT}{texto}{Style.RESET_ALL}"

def info(texto: str) -> str:
    """Formata um texto como informação."""
    return f"{Fore.BLUE}{texto}{Style.RESET_ALL}"

def sublinhado(texto: str) -> str:
    """Formata um texto como sublinhado."""
    return f"{SUBLINHADO}{texto}{RESET}"

def negrito(texto: str) -> str:
    """Formata um texto como negrito."""
    return f"{Style.BRIGHT}{texto}{Style.RESET_ALL}"

def italico(texto):
    """Formata um texto como itálico."""
    return f"{ITALICO}{texto}{RESET}"

def invertido(texto):
    """Formata um texto como invertido."""
    return f"{INVERTIDO}{texto}{RESET}"

def nota(nota):
    """Formata uma nota com cor baseada no valor."""
    if nota >= 7:
        return f"{VERDE}{nota}{RESET}"
    elif nota >= 5:
        return f"{AMARELO}{nota}{RESET}"
    else:
        return f"{VERMELHO}{nota}{RESET}"

def score(score):
    """Formata um score com cor baseada no valor."""
    if score >= 80:
        return f"{VERDE}{score}%{RESET}"
    elif score >= 60:
        return f"{AMARELO}{score}%{RESET}"
    else:
        return f"{VERMELHO}{score}%{RESET}"

def menu_item(numero: str, texto: str) -> str:
    """Formata um item de menu."""
    return f"{Fore.CYAN}{numero}{Style.RESET_ALL}. {texto}"

def separador() -> str:
    """Retorna uma linha separadora."""
    return f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}"

def cabecalho(texto: str) -> str:
    """Cria um cabeçalho formatado."""
    return f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 50}\n{texto.center(50)}\n{'=' * 50}{Style.RESET_ALL}" 