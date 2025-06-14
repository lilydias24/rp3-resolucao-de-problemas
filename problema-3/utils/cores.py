"""
Módulo para formatação de cores no terminal.
"""

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

def titulo(texto):
    """Formata um texto como título."""
    return f"{NEGRITO}{AZUL}{texto}{RESET}"

def sucesso(texto):
    """Formata um texto como mensagem de sucesso."""
    return f"{VERDE}{texto}{RESET}"

def erro(texto):
    """Formata um texto como mensagem de erro."""
    return f"{VERMELHO}{texto}{RESET}"

def aviso(texto):
    """Formata um texto como aviso."""
    return f"{AMARELO}{texto}{RESET}"

def destaque(texto):
    """Formata um texto como destaque."""
    return f"{NEGRITO}{CIANO}{texto}{RESET}"

def info(texto):
    """Formata um texto como informação."""
    return f"{MAGENTA}{texto}{RESET}"

def sublinhado(texto):
    """Formata um texto como sublinhado."""
    return f"{SUBLINHADO}{texto}{RESET}"

def negrito(texto):
    """Formata um texto como negrito."""
    return f"{NEGRITO}{texto}{RESET}"

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

def menu_item(numero, texto):
    """Formata um item de menu."""
    return f"{destaque(numero + '.')} {texto}"

def separador(char='='):
    """Cria um separador colorido."""
    return f"{AZUL}{char * 50}{RESET}"

def cabecalho(texto):
    """Cria um cabeçalho formatado."""
    return f"\n{separador()}\n{titulo(texto)}\n{separador()}" 