import hashlib

def hash_senha(senha: str) -> str:
    """gera o hash da senha usando SHA-256."""
    return hashlib.sha256(senha.encode()).hexdigest()

def normalizar_email(email: str) -> str:
    """remove espaços e converte o email p letras minúsculas."""
    return email.strip().lower()