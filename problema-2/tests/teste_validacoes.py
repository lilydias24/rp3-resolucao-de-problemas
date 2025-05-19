"""
Teste das funções de validação implementadas no módulo validacoes.py
Este script executa testes simples para verificar o comportamento das funções.
"""

from src.autenticacao.validacoes import (
    validar_nome, validar_email, validar_senha, validar_cpf,
    validar_telefone, validar_data_nascimento, formatar_cpf, formatar_telefone
)

def testar_validar_nome():
    """testa a função validar_nome com diferentes entradas"""
    print("\n=== Teste da função validar_nome ===")
    casos_teste = [
        ("João Silva", True),
        ("Ana", True),
        ("J", False),  # muito curto
        ("João123", False),  # contem numeros
        ("João@Silva", False),  # contem caracteres especiais
        (" João Silva", False),  # começa com espaço
        ("João Silva ", False),  # termina com espaço
        ("", False),  # vazio
        ("   ", False),  # apenas espaços
        ("Maria José Oliveira", True),
        ("Ângela", True),  # com acento
    ]
    
    for nome, esperado in casos_teste:
        resultado = validar_nome(nome)
        status = "✓" if resultado == esperado else "✗"
        print(f"{status} validar_nome('{nome}') = {resultado}, esperado: {esperado}")

def testar_validar_email():
    """Testa a função validar_email com diferentes entradas"""
    print("\n=== Teste da função validar_email ===")
    casos_teste = [
        ("usuario@dominio.com", True),
        ("usuario@dominio.com.br", True),  # dominio com multiplos niveis é valido
        ("usuario@dominio", False),  # sem extensão
        ("usuario.dominio.com", False),  # sem @
        ("@dominio.com", False),  # sem usuario
        ("usuario@.com", False),  # dominio invalido
        ("usuario@dominio.", False),  # extensão vazia
        ("usuario @ dominio.com", False),  # espaços
        ("", False),  # vazio
        ("usuario+teste@dominio.com", True),  # com + (valido)
        ("usuario.teste@dominio.com", True),  # com . (valido)
    ]
    
    for email, esperado in casos_teste:
        resultado = validar_email(email)
        status = "✓" if resultado == esperado else "✗"
        print(f"{status} validar_email('{email}') = {resultado}, esperado: {esperado}")

def testar_validar_senha():
    """Testa a função validar_senha com diferentes entradas"""
    print("\n=== Teste da função validar_senha ===")
    casos_teste = [
        ("Senha123", True),  # valida
        ("senha123", False),  # sem maiuscula
        ("SENHA123", False),  # sem minuscula
        ("SenhaTeste", False),  # sem numero
        ("Sen123", False),  # muito curta
        ("", False),  # vazia
        ("Senha!123", True),  # com caractere especial
        ("SenhaForteMuito2025", True),  # senha longa
    ]
    
    for senha, esperado in casos_teste:
        resultado = validar_senha(senha)
        status = "✓" if resultado == esperado else "✗"
        print(f"{status} validar_senha('{senha}') = {resultado}, esperado: {esperado}")

def testar_validar_cpf():
    """Testa a função validar_cpf com diferentes entradas"""
    print("\n=== Teste da função validar_cpf ===")
    casos_teste = [
        ("529.982.247-25", True),  # cpf valido formatado
        ("52998224725", True),  # cpf valido sem formatação
        ("111.111.111-11", False),  # cpf invalido (digitos repetidos)
        ("529.982.247-24", False),  # cpf invalido (digito verificador errado)
        ("52998224", False),  # cpf incompleto
        ("", False),  # vazio
        ("ABC.DEF.GHI-JK", False),  # nao numerico
    ]
    
    for cpf, esperado in casos_teste:
        resultado = validar_cpf(cpf)
        status = "✓" if resultado == esperado else "✗"
        print(f"{status} validar_cpf('{cpf}') = {resultado}, esperado: {esperado}")

def testar_validar_telefone():
    """Testa a função validar_telefone com diferentes entradas"""
    print("\n=== Teste da função validar_telefone ===")
    casos_teste = [
        ("(11) 98765-4321", True),  # celular formatado
        ("(11) 8765-4321", True),  # fixo formatado
        ("11987654321", True),  # celular sem formatação
        ("1187654321", True),  # fixo sem formatação
        ("(11) 7765-4321", True),  # fixo com digito diferente de 9
        ("(01) 98765-4321", False),  # ddd invalido
        ("98765-4321", False),  # sem ddd
        ("(11) 98765-432", False),  # incompleto
        ("", False),  # vazio
    ]
    
    for telefone, esperado in casos_teste:
        resultado = validar_telefone(telefone)
        status = "✓" if resultado == esperado else "✗"
        print(f"{status} validar_telefone('{telefone}') = {resultado}, esperado: {esperado}")

def testar_validar_data_nascimento():
    """Testa a função validar_data_nascimento com diferentes entradas"""
    print("\n=== Teste da função validar_data_nascimento ===")
    casos_teste = [
        ("01/01/1990", True),  # data valida
        ("01/01/2030", False),  # data futura
        ("31/02/1990", False),  # data invalida (fevereiro nao tem 31 dias)
        ("01-01-1990", False),  # formato invalido
        ("", False),  # vazio
    ]
    
    for data, esperado in casos_teste:
        resultado = validar_data_nascimento(data)
        status = "✓" if resultado == esperado else "✗"
        print(f"{status} validar_data_nascimento('{data}') = {resultado}, esperado: {esperado}")
    

    print("\n--- Teste com idade mínima ---")
    hoje = datetime.now()
    ano_atual = hoje.year
    
   
    data_18_anos = f"01/01/{ano_atual - 18}"
    resultado = validar_data_nascimento(data_18_anos, idade_minima=18)
    print(f"✓ Pessoa com 18 anos: {resultado}")
    

    data_17_anos = f"01/01/{ano_atual - 17}"
    resultado = validar_data_nascimento(data_17_anos, idade_minima=18)
    print(f"✓ Pessoa com 17 anos (idade mínima 18): {resultado}")

def testar_formatar_cpf():
    """testa a função formatar_cpf com diferentes entradas"""
    print("\n=== Teste da função formatar_cpf ===")
    casos_teste = [
        ("52998224725", "529.982.247-25"),
        ("529.982.247-25", "529.982.247-25"),
        ("5299822472", ""),  # incompleto
        ("", ""),  # vazio
    ]
    
    for cpf, esperado in casos_teste:
        resultado = formatar_cpf(cpf)
        status = "✓" if resultado == esperado else "✗"
        print(f"{status} formatar_cpf('{cpf}') = '{resultado}', esperado: '{esperado}'")

def testar_formatar_telefone():
    """Testa a função formatar_telefone com diferentes entradas"""
    print("\n=== Teste da função formatar_telefone ===")
    casos_teste = [
        ("11987654321", "(11) 98765-4321"),  # celular
        ("1187654321", "(11) 8765-4321"),  # fixo
        ("(11) 98765-4321", "(11) 98765-4321"),  # ja formatado
        ("11-98765-4321", "(11) 98765-4321"),  # com hifen
        ("987654321", ""),  # incompleto
        ("", ""),  # vazio
    ]
    
    for telefone, esperado in casos_teste:
        resultado = formatar_telefone(telefone)
        status = "✓" if resultado == esperado else "✗"
        print(f"{status} formatar_telefone('{telefone}') = '{resultado}', esperado: '{esperado}'")

if __name__ == "__main__":
    print("=== testes das funções de validação ===")
    
    from datetime import datetime
    
    testar_validar_nome()
    testar_validar_email()
    testar_validar_senha()
    testar_validar_cpf()
    testar_validar_telefone()
    testar_validar_data_nascimento()
    testar_formatar_cpf()
    testar_formatar_telefone()
    
    print("\ntestes concluídos!") 