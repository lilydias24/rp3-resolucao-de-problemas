import re

def validar_nome(nome: str) -> bool:
    """ve se o nome tem pelo menos 3 caracteres"""
    return len(nome.strip()) >= 3

def validar_email(email: str) -> bool:
    """ve se o email está em um formato válido"""
    padrao_email = r"[^@]+@[^@]+\.[^@]+"
    return re.match(padrao_email, email) is not None

def validar_senha(senha: str) -> bool:
    """ve se a senha tem pelo menos 8 caracteres"""
    return len(senha) >= 8