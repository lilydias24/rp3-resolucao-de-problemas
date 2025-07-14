import csv
import os
from typing import Dict, List, Optional, Tuple
from src.autenticacao.utilitarios import hash_senha, normalizar_email

Conta = Dict[str, str]


def validar_dados(nome: str, email: str, senha: str) -> Tuple[bool, str]:
    """Valida os dados de uma nova conta.

    Args:
        nome (str): Nome do usuário.
        email (str): Email do usuário.
        senha (str): Senha do usuário.

    Returns:
        Tuple[bool, str]: Resultado da validação (True/False) e mensagem de erro (se houver).
    """
    return (
        (False, "Todos os campos são obrigatórios")
        if not nome or not email or not senha
        else (
            (False, "A senha deve ter pelo menos 8 caracteres")
            if len(senha) < 8
            else (True, "")
        )
    )


def gerar_id(contas: List[Conta]) -> str:
    """Gera um novo ID para uma nova conta.

    Args:
        contas (List[Conta]): Lista de contas existentes.

    Returns:
        str: Novo ID gerado.
    """
    return str(max(map(lambda c: int(c["id"]), contas), default=0) + 1)


def email_disponivel(email: str, contas: List[Conta]) -> bool:
    """Verifica se o email já está em uso.

    Args:
        email (str): Email a ser verificado.
        contas (List[Conta]): Lista de contas existentes.

    Returns:
        bool: True se o email estiver disponível, False se já existir.
    """
    return not any(c["email"] == email for c in contas)


def criar_conta_dict(id_: str, nome: str, email: str, senha: str) -> Conta:
    """Cria o dicionário representando uma conta.

    Args:
        id_ (str): ID da conta.
        nome (str): Nome do usuário.
        email (str): Email do usuário.
        senha (str): Senha do usuário.

    Returns:
        Conta: Dicionário contendo os dados da conta.
    """
    return {
        "id": id_,
        "nome": nome,
        "email": normalizar_email(email),
        "senha_hash": hash_senha(senha),
    }


def conta_para_linha_csv(conta: Conta) -> List[str]:
    """Converte uma conta para uma linha de CSV.

    Args:
        conta (Conta): Dicionário da conta.

    Returns:
        List[str]: Lista de valores para escrever no CSV.
    """
    return list(map(conta.get, ["id", "nome", "email", "senha_hash"]))


def linha_csv_para_conta(linha: Dict[str, str]) -> Conta:
    """Converte uma linha do CSV em um dicionário de conta.

    Args:
        linha (Dict[str, str]): Linha lida do CSV.

    Returns:
        Conta: Conta reconstruída a partir da linha.
    """
    return {chave: linha[chave] for chave in ["id", "nome", "email", "senha_hash"]}


def editar_conta_lista(
    contas: List[Conta],
    id_alvo: str,
    novo_nome: Optional[str],
    novo_email: Optional[str],
    nova_senha: Optional[str],
) -> List[Conta]:
    """Edita uma conta existente na lista.

    Args:
        contas (List[Conta]): Lista de contas existentes.
        id_alvo (str): ID da conta a ser editada.
        novo_nome (Optional[str]): Novo nome (ou None para manter o atual).
        novo_email (Optional[str]): Novo email (ou None para manter o atual).
        nova_senha (Optional[str]): Nova senha (ou None para manter a atual).

    Returns:
        List[Conta]: Lista de contas atualizada.
    """
    return list(
        map(
            lambda conta: (
                {
                    **conta,
                    "nome": novo_nome or conta["nome"],
                    "email": (
                        normalizar_email(novo_email) if novo_email else conta["email"]
                    ),
                    "senha_hash": (
                        hash_senha(nova_senha) if nova_senha else conta["senha_hash"]
                    ),
                }
                if conta["id"] == id_alvo
                else conta
            ),
            contas,
        )
    )


def excluir_conta_lista(contas: List[Conta], id_alvo: str) -> List[Conta]:
    """Exclui uma conta da lista de contas.

    Args:
        contas (List[Conta]): Lista de contas existentes.
        id_alvo (str): ID da conta a ser excluída.

    Returns:
        List[Conta]: Lista de contas sem a conta excluída.
    """
    return list(filter(lambda conta: conta["id"] != id_alvo, contas))


# ---------- Entrada/Saída isolada ----------


def carregar_contas(caminho: str) -> List[Conta]:
    """Carrega as contas de um arquivo CSV.

    Args:
        caminho (str): Caminho para o arquivo CSV.

    Returns:
        List[Conta]: Lista de contas carregadas.
    """
    return (
        []
        if not os.path.exists(caminho)
        else list(
            map(
                linha_csv_para_conta,
                csv.DictReader(open(caminho, mode="r", encoding="utf-8")),
            )
        )
    )


def salvar_contas(caminho: str, contas: List[Conta]) -> None:
    """Salva a lista de contas em um arquivo CSV.

    Args:
        caminho (str): Caminho para o arquivo CSV.
        contas (List[Conta]): Lista de contas a serem salvas.
    """
    with open(caminho, mode="w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(
            arquivo, fieldnames=["id", "nome", "email", "senha_hash"]
        )
        escritor.writeheader()
        escritor.writerows(contas)


# ---------- Orquestração funcional ----------


def criar_conta(caminho: str, nome: str, email: str, senha: str) -> Tuple[bool, str]:
    """Cria uma nova conta e salva no arquivo.

    Args:
        caminho (str): Caminho para o arquivo CSV.
        nome (str): Nome do usuário.
        email (str): Email do usuário.
        senha (str): Senha do usuário.

    Returns:
        Tuple[bool, str]: Resultado da criação (True/False) e mensagem.
    """
    contas = carregar_contas(caminho)
    email_normalizado = normalizar_email(email)

    valido, mensagem = validar_dados(nome, email_normalizado, senha)
    if not valido:
        return (False, mensagem)

    if not email_disponivel(email_normalizado, contas):
        return (False, "Email já está em uso")

    return _salvar_e_retorna_sucesso(contas, caminho, nome, email_normalizado, senha)


def _salvar_e_retorna_sucesso(
    contas: List[Conta], caminho: str, nome: str, email: str, senha: str
) -> Tuple[bool, str]:
    """Salva a nova conta e retorna mensagem de sucesso.

    Args:
        contas (List[Conta]): Lista de contas existente.
        caminho (str): Caminho do arquivo CSV.
        nome (str): Nome do usuário.
        email (str): Email do usuário.
        senha (str): Senha do usuário.

    Returns:
        Tuple[bool, str]: Resultado da operação.
    """
    novo_id = gerar_id(contas)
    nova_conta = criar_conta_dict(novo_id, nome, email, senha)
    contas_atualizadas = contas + [nova_conta]
    salvar_contas(caminho, contas_atualizadas)
    return (True, "Conta criada com sucesso")


def buscar_conta_por_id(caminho: str, id_: str) -> Optional[Conta]:
    """Busca uma conta pelo ID.

    Args:
        caminho (str): Caminho do arquivo CSV.
        id_ (str): ID da conta.

    Returns:
        Optional[Conta]: Conta encontrada ou None se não existir.
    """
    return next(filter(lambda c: c["id"] == id_, carregar_contas(caminho)), None)


def editar_conta(
    caminho: str,
    id_alvo: str,
    novo_nome: Optional[str],
    novo_email: Optional[str],
    nova_senha: Optional[str],
) -> Tuple[bool, str]:
    """Edita os dados de uma conta existente.

    Args:
        caminho (str): Caminho do arquivo CSV.
        id_alvo (str): ID da conta a ser editada.
        novo_nome (Optional[str]): Novo nome.
        novo_email (Optional[str]): Novo email.
        nova_senha (Optional[str]): Nova senha.

    Returns:
        Tuple[bool, str]: Resultado da operação.
    """
    contas = carregar_contas(caminho)

    if not any(conta["id"] == id_alvo for conta in contas):
        return (False, "Conta não encontrada")

    contas_atualizadas = editar_conta_lista(
        contas, id_alvo, novo_nome, novo_email, nova_senha
    )
    salvar_contas(caminho, contas_atualizadas)
    return (True, "Conta atualizada com sucesso")


def excluir_conta(caminho: str, id_alvo: str) -> Tuple[bool, str]:
    """Exclui uma conta existente.

    Args:
        caminho (str): Caminho do arquivo CSV.
        id_alvo (str): ID da conta a ser excluída.

    Returns:
        Tuple[bool, str]: Resultado da operação.
    """
    contas = carregar_contas(caminho)

    if not any(conta["id"] == id_alvo for conta in contas):
        return (False, "Conta não encontrada")

    contas_atualizadas = excluir_conta_lista(contas, id_alvo)
    salvar_contas(caminho, contas_atualizadas)
    return (True, "Conta excluída com sucesso")
