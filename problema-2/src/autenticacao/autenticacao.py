import csv
from typing import Tuple, List, Dict, Iterable
from utilitarios import hash_senha, normalizar_email
from validacoes import validar_nome, validar_email, validar_senha

Conta = Dict[str, str]

def carregar_contas(caminho: str) -> List[Conta]:
    """carrega as contas do arquivo csv como uma lista imutável"""
    try:
        with open(caminho, mode="r", encoding="utf-8") as arquivo:
            return list(csv.DictReader(arquivo))
    except FileNotFoundError:
        return []

def salvar_contas(caminho: str, contas: Iterable[Conta]) -> None:
    """Salva as contas no arquivo CSV."""
    with open(caminho, mode="w", newline="", encoding="utf-8") as arquivo:
        campos = ["id", "nome", "email", "senha_hash"]
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
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

def email_existe(contas: Iterable[Conta], email_normalizado: str) -> bool:
    """Verifica se o email já existe nas contas."""
    return any(map(lambda conta: conta["email"] == email_normalizado, contas))

def criar_conta(caminho: str, nome: str, email: str, senha: str) -> Tuple[bool, str, List[Conta]]:
    """cria uma nova conta depois das validações e retorna a nova lista de contas"""
    contas = carregar_contas(caminho)
    email_normalizado = normalizar_email(email)

    validacoes = [
        (validar_nome(nome), "nome inválido. Deve ter pelo menos 3 caracteres."),
        (validar_email(email), "email inválido."),
        (validar_senha(senha), "senha inválida. Deve ter pelo menos 8 caracteres."),
        (not email_existe(contas, email_normalizado), "email já está em uso.")
    ]

    erros = filter(lambda v: not v[0], validacoes)
    erro = next(map(lambda v: (False, v[1], contas), erros), None)

    if erro:
        return erro

    nova_conta = criar_conta_dict(str(len(contas) + 1), nome, email, senha)
    return True, "conta criada com sucesso!", contas + [nova_conta]

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