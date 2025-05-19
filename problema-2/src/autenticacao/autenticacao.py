import csv
from typing import Tuple, List, Dict, Iterable
from .utilitarios import hash_senha, normalizar_email
from .validacoes import validar_email, validar_nome, validar_senha
from ..administracao.gerenciarConta import (
    salvar_contas, carregar_contas, criar_conta_dict,
    email_disponivel, criar_conta
)

def login(caminho: str, email: str, senha: str) -> Tuple[bool, str]:
    """Realiza o login verificando se email e senha batem com alguma conta."""
    contas = carregar_contas(caminho)
    email_normalizado = normalizar_email(email)
    senha_hash = hash_senha(senha)

    conta = next(
        filter(lambda c: c["email"] == email_normalizado and c["senha_hash"] == senha_hash, contas),
        None
    )

    return (
        (True, f"Login bem-sucedido! Bem-vindo(a), {conta['nome']}.") if conta
        else (False, "Email ou senha incorretos.")
    )