import re

def validar_nome(nome: str) -> bool:
    """Retorna True se o nome tiver ao menos 3 caracteres não vazios."""
    return len(nome.strip()) >= 3

def validar_email(email: str) -> bool:
    """Retorna True se o e-mail estiver em um formato válido."""
    padrao_email = r"[^@]+@[^@]+\.[^@]+"
    return re.match(padrao_email, email) is not None

def validar_senha(senha: str) -> bool:
    """Retorna True se a senha tiver pelo menos 8 caracteres."""
    return len(senha) >= 8