"""
Utilitários de cores para o CLI.
Fornece funções para formatação colorida de texto no terminal.
"""
from colorama import init, Fore, Back, Style

# Inicializar colorama para compatibilidade com Windows
init(autoreset=True)

class Colors:
    """Classe com constantes de cores para uso no CLI"""
    
    # Cores de texto
    BLACK = Fore.BLACK
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    
    # Cores de fundo
    BG_BLACK = Back.BLACK
    BG_RED = Back.RED
    BG_GREEN = Back.GREEN
    BG_YELLOW = Back.YELLOW
    BG_BLUE = Back.BLUE
    BG_MAGENTA = Back.MAGENTA
    BG_CYAN = Back.CYAN
    BG_WHITE = Back.WHITE
    
    # Estilos
    BRIGHT = Style.BRIGHT
    DIM = Style.DIM
    NORMAL = Style.NORMAL
    RESET = Style.RESET_ALL

class CLIFormatter:
    """Classe para formatação de texto no CLI"""
    
    @staticmethod
    def header(text: str) -> str:
        """Formata um cabeçalho colorido"""
        return f"\n{Colors.CYAN}{Colors.BRIGHT}{'='*60}\n{Colors.CYAN}{Colors.BRIGHT}{text.center(60)}\n{Colors.CYAN}{Colors.BRIGHT}{'='*60}{Colors.RESET}"
    
    @staticmethod
    def success(text: str) -> str:
        """Formata mensagem de sucesso em verde"""
        return f"{Colors.GREEN}✓ {text}{Colors.RESET}"
    
    @staticmethod
    def error(text: str) -> str:
        """Formata mensagem de erro em vermelho"""
        return f"{Colors.RED}✗ {text}{Colors.RESET}"
    
    @staticmethod
    def warning(text: str) -> str:
        """Formata mensagem de aviso em amarelo"""
        return f"{Colors.YELLOW}⚠ {text}{Colors.RESET}"
    
    @staticmethod
    def info(text: str) -> str:
        """Formata informação em azul"""
        return f"{Colors.BLUE}ℹ {text}{Colors.RESET}"
    
    @staticmethod
    def menu_title(text: str) -> str:
        """Formata título do menu em magenta"""
        return f"\n{Colors.MAGENTA}{Colors.BRIGHT}--- {text} ---{Colors.RESET}"
    
    @staticmethod
    def menu_option(number: str, text: str) -> str:
        """Formata opção do menu com número destacado"""
        return f"{Colors.WHITE}{number} - {text}{Colors.RESET}"
    
    @staticmethod
    def separator() -> str:
        """Formata separador colorido"""
        return f"{Colors.CYAN}{'─'*50}{Colors.RESET}"
    
    @staticmethod
    def highlight(text: str) -> str:
        """Destaca texto em branco brilhante"""
        return f"{Colors.WHITE}{Colors.BRIGHT}{text}{Colors.RESET}"
    
    @staticmethod
    def muted(text: str) -> str:
        """Formata texto em cor suave"""
        return f"{Colors.WHITE}{Colors.DIM}{text}{Colors.RESET}"
    
    @staticmethod
    def accent(text: str) -> str:
        """Formata texto em cor de destaque (ciano)"""
        return f"{Colors.CYAN}{text}{Colors.RESET}"
    
    @staticmethod
    def primary(text: str) -> str:
        """Formata texto em cor primária (azul)"""
        return f"{Colors.BLUE}{Colors.BRIGHT}{text}{Colors.RESET}"
    
    @staticmethod
    def secondary(text: str) -> str:
        """Formata texto em cor secundária (magenta)"""
        return f"{Colors.MAGENTA}{text}{Colors.RESET}"

# Funções de conveniência para uso direto
def print_header(text: str):
    """Imprime um cabeçalho colorido"""
    print(CLIFormatter.header(text))

def print_success(text: str):
    """Imprime mensagem de sucesso em verde"""
    print(CLIFormatter.success(text))

def print_error(text: str):
    """Imprime mensagem de erro em vermelho"""
    print(CLIFormatter.error(text))

def print_warning(text: str):
    """Imprime mensagem de aviso em amarelo"""
    print(CLIFormatter.warning(text))

def print_info(text: str):
    """Imprime informação em azul"""
    print(CLIFormatter.info(text))

def print_menu_title(text: str):
    """Imprime título do menu em magenta"""
    print(CLIFormatter.menu_title(text))

def print_menu_option(number: str, text: str):
    """Imprime opção do menu com número destacado"""
    print(CLIFormatter.menu_option(number, text))

def print_separator():
    """Imprime separador colorido"""
    print(CLIFormatter.separator())

def print_highlight(text: str):
    """Imprime texto destacado"""
    print(CLIFormatter.highlight(text))

def print_muted(text: str):
    """Imprime texto em cor suave"""
    print(CLIFormatter.muted(text))

def print_accent(text: str):
    """Imprime texto em cor de destaque"""
    print(CLIFormatter.accent(text))

def print_primary(text: str):
    """Imprime texto em cor primária"""
    print(CLIFormatter.primary(text))

def print_secondary(text: str):
    """Imprime texto em cor secundária"""
    print(CLIFormatter.secondary(text))

# Funções para formatação de dados específicos
def format_id(id_value: str) -> str:
    """Formata ID em cor destacada"""
    return f"{Colors.CYAN}{Colors.BRIGHT}ID: {id_value}{Colors.RESET}"

def format_name(name: str) -> str:
    """Formata nome em cor primária"""
    return f"{Colors.BLUE}{Colors.BRIGHT}{name}{Colors.RESET}"

def format_status(status: str) -> str:
    """Formata status com cor apropriada"""
    status_lower = status.lower()
    if status_lower in ['approved', 'aprovado', 'success']:
        return f"{Colors.GREEN}{status}{Colors.RESET}"
    elif status_lower in ['rejected', 'rejeitado', 'error']:
        return f"{Colors.RED}{status}{Colors.RESET}"
    elif status_lower in ['pending', 'pendente', 'warning']:
        return f"{Colors.YELLOW}{status}{Colors.RESET}"
    else:
        return f"{Colors.WHITE}{status}{Colors.RESET}"

def format_priority(priority: int) -> str:
    """Formata prioridade com cor baseada no valor"""
    if priority >= 4:
        return f"{Colors.RED}{Colors.BRIGHT}P{priority}{Colors.RESET}"
    elif priority >= 2:
        return f"{Colors.YELLOW}P{priority}{Colors.RESET}"
    else:
        return f"{Colors.GREEN}P{priority}{Colors.RESET}"

def format_timestamp(timestamp: str) -> str:
    """Formata timestamp em cor suave"""
    return f"{Colors.WHITE}{Colors.DIM}{timestamp}{Colors.RESET}"

def format_description(description: str) -> str:
    """Formata descrição em cor normal"""
    return f"{Colors.WHITE}{description}{Colors.RESET}"

# Funções para listas e tabelas
def format_list_item(index: int, text: str) -> str:
    """Formata item de lista com índice colorido"""
    return f"{Colors.CYAN}{index}.{Colors.RESET} {text}"

def format_table_header(headers: list) -> str:
    """Formata cabeçalho de tabela"""
    header_text = " | ".join(headers)
    return f"{Colors.MAGENTA}{Colors.BRIGHT}{header_text}{Colors.RESET}"

def format_table_row(values: list) -> str:
    """Formata linha de tabela"""
    return " | ".join(str(value) for value in values)

# Funções para progresso e loading
def print_loading(text: str):
    """Imprime mensagem de carregamento"""
    print(f"{Colors.YELLOW}⏳ {text}...{Colors.RESET}")

def print_done(text: str):
    """Imprime mensagem de conclusão"""
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

def print_processing(text: str):
    """Imprime mensagem de processamento"""
    print(f"{Colors.BLUE}🔄 {text}{Colors.RESET}")

# Funções para seções específicas
def print_section_header(text: str):
    """Imprime cabeçalho de seção"""
    print(f"\n{Colors.CYAN}{Colors.BRIGHT}📋 {text}{Colors.RESET}")
    print(f"{Colors.CYAN}{'─' * (len(text) + 4)}{Colors.RESET}")

def print_subsection_header(text: str):
    """Imprime cabeçalho de subseção"""
    print(f"\n{Colors.MAGENTA}📌 {text}{Colors.RESET}")

def print_field_label(label: str) -> str:
    """Formata label de campo"""
    return f"{Colors.CYAN}{label}:{Colors.RESET}"

def print_field_value(value: str) -> str:
    """Formata valor de campo"""
    return f"{Colors.WHITE}{value}{Colors.RESET}" 