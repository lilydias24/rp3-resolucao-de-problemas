import csv
import hashlib
import os
from typing import Dict, List, Optional, Tuple

# Tipos
Conta = Dict[str, str]


def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

def validar_dados(nome: str, email: str, senha: str) -> Tuple[bool, str]:
    return (
        (False, "Todos os campos são obrigatórios") if not nome or not email or not senha else
        (False, "A senha deve ter pelo menos 8 caracteres") if len(senha) < 8 else
        (True, "")
    )

def normalizar_email(email: str) -> str:
    return email.strip().lower()

def gerar_id(contas: List[Conta]) -> str:
    return str(max(map(lambda c: int(c["id"]), contas), default=0) + 1)

def email_disponivel(email: str, contas: List[Conta]) -> bool:
    return not any(c["email"] == email for c in contas)

def criar_conta_dict(id_: str, nome: str, email: str, senha: str) -> Conta:
    return {
        "id": id_,
        "nome": nome,
        "email": normalizar_email(email),
        "senha_hash": hash_senha(senha)
    }

def conta_para_linha_csv(conta: Conta) -> List[str]:
    return list(map(conta.get, ["id", "nome", "email", "senha_hash"]))

def linha_csv_para_conta(linha: Dict[str, str]) -> Conta:
    return {chave: linha[chave] for chave in ["id", "nome", "email", "senha_hash"]}

# ---------- Entrada/Saída isolada ----------

def carregar_contas(caminho: str) -> List[Conta]:
    return (
        [] if not os.path.exists(caminho) else
        list(map(linha_csv_para_conta, csv.DictReader(open(caminho, mode="r", encoding="utf-8"))))
    )

def salvar_contas(caminho: str, contas: List[Conta]) -> None:
    with open(caminho, mode="w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=["id", "nome", "email", "senha_hash"])
        escritor.writeheader()
        escritor.writerows(contas)

# ---------- Orquestração funcional ----------

def criar_conta(caminho: str, nome: str, email: str, senha: str) -> Tuple[bool, str]:
    contas = carregar_contas(caminho)
    email_normalizado = normalizar_email(email)

    return (
        validar_dados(nome, email_normalizado, senha)
        if not validar_dados(nome, email_normalizado, senha)[0] else
        (False, "Email já está em uso") if not email_disponivel(email_normalizado, contas) else
        _salvar_e_retorna_sucesso(contas, caminho, nome, email_normalizado, senha)
    )

def _salvar_e_retorna_sucesso(contas: List[Conta], caminho: str, nome: str, email: str, senha: str) -> Tuple[bool, str]:
    novo_id = gerar_id(contas)
    nova_conta = criar_conta_dict(novo_id, nome, email, senha)
    contas_atualizadas = contas + [nova_conta]
    salvar_contas(caminho, contas_atualizadas)
    return (True, "Conta criada com sucesso")

def buscar_conta_por_id(caminho: str, id_: str) -> Optional[Conta]:
    return next(filter(lambda c: c["id"] == id_, carregar_contas(caminho)), None)

