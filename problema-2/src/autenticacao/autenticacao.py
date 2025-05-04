import csv
from utilitarios import hash_senha, normalizar_email
from validacoes import validar_nome, validar_email, validar_senha
from typing import Tuple, List, Dict

Conta = Dict[str, str]

def carregar_contas(caminho: str) -> List[Conta]:
    """carrega as contas do arquivo csv como uma lista imutável"""
    try:
        with open(caminho, mode="r", encoding="utf-8") as arquivo:
            return list(csv.DictReader(arquivo))
    except FileNotFoundError:
        return []

def salvar_contas(caminho: str, contas: List[Conta]) -> None:
    """salva as contas no arquivo csv"""
    with open(caminho, mode="w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=["id", "nome", "email", "senha_hash"])
        escritor.writeheader()
        escritor.writerows(contas)

def criar_conta_dict(id_: str, nome: str, email: str, senha: str) -> Conta:
    """cria um dicionário de conta"""
    return {
        "id": id_,
        "nome": nome,
        "email": normalizar_email(email),
        "senha_hash": hash_senha(senha),
    }

def criar_conta(caminho: str, nome: str, email: str, senha: str) -> Tuple[bool, str, List[Conta]]:
    """cria uma nova conta depois das validações e retorna a nova lista de contas"""
    contas = carregar_contas(caminho)
    email_normalizado = normalizar_email(email)

    if not validar_nome(nome):
        return False, "nome inválido. Deve ter pelo menos 3 caracteres.", contas
    if not validar_email(email):
        return False, "email inválido.", contas
    if not validar_senha(senha):
        return False, "senha inválida. Deve ter pelo menos 8 caracteres.", contas
    if any(c["email"] == email_normalizado for c in contas):
        return False, "email já está em uso.", contas

    nova_conta = criar_conta_dict(str(len(contas) + 1), nome, email, senha)
    novas_contas = contas + [nova_conta]  
    return True, "conta criada com sucesso!", novas_contas

def login(caminho: str, email: str, senha: str) -> Tuple[bool, str]:
    """faz o login de um usuário."""
    contas = carregar_contas(caminho)
    email_normalizado = normalizar_email(email)
    senha_hash = hash_senha(senha)

    conta_encontrada = next(
        (conta for conta in contas if conta["email"] == email_normalizado and conta["senha_hash"] == senha_hash),
        None
    )
    if conta_encontrada:
        return True, f"Login bem-sucedido! Bem-vindo(a), {conta_encontrada['nome']}."
    return False, "Email ou senha incorretos."