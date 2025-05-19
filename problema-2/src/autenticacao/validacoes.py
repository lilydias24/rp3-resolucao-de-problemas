import re
from datetime import datetime
from typing import Optional

def validar_nome(nome: str) -> bool:
    """
    Valida um nome de usuário.
    
    Regras:
    - Deve ter pelo menos 3 caracteres
    - Deve conter apenas letras e espaços
    - Não deve começar ou terminar com espaço
    
    Args:
        nome: O nome a ser validado
    
    Returns:
        True se o nome for válido, False caso contrário
    """
    if not nome or len(nome.strip()) < 3:
        return False
    
    # verifica se contém apenas letras e espaços
    if not re.match(r'^[A-Za-zÀ-ÖØ-öø-ÿ ]+$', nome):
        return False
    
    # verifica se não começa ou termina com espaço
    return nome == nome.strip()

def validar_email(email: str) -> bool:
    """
    valida um endereço de e-mail.
    
    Regras:
    - Deve seguir o formato padrão de e-mail (usuário@domínio)
    - Domínio deve ter pelo menos um nível (com extensão)
    - A última extensão deve ter entre 2 e 4 caracteres (como .com, .org, .br)
    
    Args:
        email: O e-mail a ser validado
    
    Returns:
        True se o e-mail for válido, False caso contrário
    """
    if not email or '@' not in email:
        return False
    
    # extrai a parte do usuário e do domínio
    try:
        usuario, dominio = email.split('@', 1)
    except ValueError:
        return False
    
    # verifica se o usuário e o domínio não estão vazios
    if not usuario or not dominio:
        return False
    
    # verifica se o domínio tem pelo menos um ponto
    if '.' not in dominio:
        return False
    
    # verifica se a última parte do domínio (TLD) tem entre 2-4 caracteres
    partes_dominio = dominio.split('.')
    if not 2 <= len(partes_dominio[-1]) <= 4:
        return False
    
    # valida o formato completo com regex
    padrao_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}(\.([a-zA-Z]{2,4}))?$'
    if not re.match(padrao_email, email):
        return False
        
    return True

def validar_senha(senha: str) -> bool:
    """
    valida uma senha.
    
    Regras:
    - Deve ter pelo menos 8 caracteres
    - Deve conter pelo menos uma letra maiúscula
    - Deve conter pelo menos uma letra minúscula
    - Deve conter pelo menos um número
    
    Args:
        senha: A senha a ser validada
    
    Returns:
        true se a senha for válida, false caso contrário
    """
    if not senha or len(senha) < 8:
        return False
    
    # verifica requisitos de segurança
    tem_maiuscula = any(c.isupper() for c in senha)
    tem_minuscula = any(c.islower() for c in senha)
    tem_numero = any(c.isdigit() for c in senha)
    
    return tem_maiuscula and tem_minuscula and tem_numero

def validar_cpf(cpf: str) -> bool:
    """
    valida um CPF.
    
    Regras:
    - Deve ter 11 dígitos (apenas números)
    - Deve ser um CPF válido (algoritmo de verificação de dígitos)
    
    Args:
        cpf: O CPF a ser validado (com ou sem formatação)
    
    Returns:
        true se o CPF for válido, false caso contrário
    """
    # Remove caracteres não numéricos
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    # verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # verifica se todos os dígitos são iguais (CPF inválido)
    if len(set(cpf)) == 1:
        return False
    
    # verificação do primeiro dígito
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    
    resto = soma % 11
    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto
    
    if int(cpf[9]) != digito1:
        return False
    
    # verificação do segundo dígito
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    
    resto = soma % 11
    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto
    
    return int(cpf[10]) == digito2

def validar_telefone(telefone: str) -> bool:
    """
    valida um número de telefone brasileiro.
    
    Regras:
    - Deve ter exatamente 10 dígitos (fixo) ou 11 dígitos (celular)
    - Se for celular, o primeiro dígito após o DDD deve ser 9
    - DDD deve estar entre 11 e 99
    
    Args:
        telefone: O número de telefone a ser validado
    
    Returns:
        True se o telefone for válido, False caso contrário
    """
    # remove caracteres não numéricos
    numero = re.sub(r'[^0-9]', '', telefone)

    # verifica o tamanho exato (com ddd)
    if len(numero) not in [10, 11]:
        return False
    
    # se for celular (11 dígitos), o primeiro dígito após o ddd deve ser 9
    if len(numero) == 11 and numero[2] != '9':
        return False
    
    # telefone fixo (10 dígitos) precisa começar com dígito válido (diferente de 9)
    if len(numero) == 10 and numero[2] == '9':
        return False
        
    # verifica o ddd (válido entre 11 e 99)
    try:
        ddd = int(numero[:2])
        if ddd < 11 or ddd > 99:
            return False
    except ValueError:
        return False
    
    return True

def validar_data_nascimento(data: str, idade_minima: Optional[int] = None) -> bool:
    """
    valida uma data de nascimento.
    
    Regras:
    - Deve estar no formato DD/MM/AAAA
    - Deve ser uma data válida
    - Se idade_minima for especificada, verifica se a pessoa tem pelo menos essa idade
    
    Args:
        data: A data de nascimento a ser validada
        idade_minima: Idade mínima exigida (opcional)
    
    Returns:
        True se a data for válida, False caso contrário
    """
    try:
        # verifica o formato
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', data):
            return False
        
        # converte para objeto de data
        dia, mes, ano = map(int, data.split('/'))
        data_nascimento = datetime(ano, mes, dia)
        
        # verifica se é uma data passada
        if data_nascimento >= datetime.now():
            return False
        
        # verifica idade mínima, se especificada
        if idade_minima is not None:
            hoje = datetime.now()
            idade = hoje.year - data_nascimento.year
            
            # ajusta a idade se ainda não fez aniversário este ano
            if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
                idade -= 1
                
            if idade < idade_minima:
                return False
        
        return True
    except ValueError:
        # data inválida (ex: 31/02/2000)
        return False

def formatar_cpf(cpf: str) -> str:
    """
    formata um cpf para o padrão brasileiro (XXX.XXX.XXX-XX).
    
    Args:
        cpf: O CPF a ser formatado (apenas números)
    
    Returns:
        CPF formatado ou string vazia se inválido
    """
    # remove caracteres não numéricos
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    if len(cpf) != 11:
        return ""
    
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def formatar_telefone(telefone: str) -> str:
    """
    formata um telefone para o padrão brasileiro.
    
    Args:
        telefone: O telefone a ser formatado (apenas números)
    
    Returns:
        Telefone formatado ou string vazia se inválido
    """
    # remove caracteres não numéricos
    numero = re.sub(r'[^0-9]', '', telefone)
    
    if len(numero) == 11:  # Celular com DDD
        return f"({numero[:2]}) {numero[2:7]}-{numero[7:]}"
    elif len(numero) == 10:  # Fixo com DDD
        return f"({numero[:2]}) {numero[2:6]}-{numero[6:]}"
    else:
        return ""