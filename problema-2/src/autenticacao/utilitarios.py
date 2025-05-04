import hashlib

def hash_senha(senha: str) -> str:
    """Gera o hash SHA-256 da senha de forma pura."""
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

def normalizar_email(email: str) -> str:
    """remove espaços e converte o email p letras minúsculas."""
    return email.strip().lower()