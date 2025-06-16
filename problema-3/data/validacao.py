"""
Módulo de validação e sanitização de dados do estudante.
"""
import re
from typing import Dict, List, Any, Tuple

class ValidacaoErro(Exception):
    """Exceção personalizada para erros de validação."""
    pass

def sanitizar_nome(nome: str) -> str:
    """
    Sanitiza o nome do estudante.
    
    Args:
        nome: Nome a ser sanitizado
        
    Returns:
        Nome sanitizado
        
    Raises:
        ValidacaoErro: Se o nome for inválido
    """
    if not nome or not isinstance(nome, str):
        raise ValidacaoErro("Nome inválido")
    
    # Remove espaços extras e caracteres especiais
    nome = re.sub(r'[^\w\s]', '', nome.strip())
    
    if len(nome) < 3:
        raise ValidacaoErro("Nome deve ter pelo menos 3 caracteres")
    
    if len(nome) > 100:
        raise ValidacaoErro("Nome deve ter no máximo 100 caracteres")
    
    return nome

def validar_interesses(interesses: List[str]) -> List[str]:
    """
    Valida a lista de interesses.
    
    Args:
        interesses: Lista de interesses a ser validada
        
    Returns:
        Lista de interesses validados
        
    Raises:
        ValidacaoErro: Se a lista for inválida
    """
    if not isinstance(interesses, list):
        raise ValidacaoErro("Interesses devem ser uma lista")
    
    interesses_validos = []
    for interesse in interesses:
        if not isinstance(interesse, str):
            continue
        
        interesse = interesse.strip()
        if interesse and len(interesse) <= 50:
            interesses_validos.append(interesse)
    
    if not interesses_validos:
        raise ValidacaoErro("Pelo menos um interesse válido é necessário")
    
    return interesses_validos

def validar_habilidades(habilidades: List[str]) -> List[str]:
    """
    Valida a lista de habilidades.
    
    Args:
        habilidades: Lista de habilidades a ser validada
        
    Returns:
        Lista de habilidades validadas
        
    Raises:
        ValidacaoErro: Se a lista for inválida
    """
    if not isinstance(habilidades, list):
        raise ValidacaoErro("Habilidades devem ser uma lista")
    
    habilidades_validas = []
    for habilidade in habilidades:
        if not isinstance(habilidade, str):
            continue
        
        habilidade = habilidade.strip()
        if habilidade and len(habilidade) <= 50:
            habilidades_validas.append(habilidade)
    
    if not habilidades_validas:
        raise ValidacaoErro("Pelo menos uma habilidade válida é necessária")
    
    return habilidades_validas

def validar_desempenho(desempenho: Dict[str, float]) -> Dict[str, float]:
    """
    Valida o dicionário de desempenho acadêmico.
    
    Args:
        desempenho: Dicionário de desempenho a ser validado
        
    Returns:
        Dicionário de desempenho validado
        
    Raises:
        ValidacaoErro: Se o dicionário for inválido
    """
    if not isinstance(desempenho, dict):
        raise ValidacaoErro("Desempenho deve ser um dicionário")
    
    desempenho_validado = {}
    for disciplina, nota in desempenho.items():
        if not isinstance(disciplina, str) or not isinstance(nota, (int, float)):
            continue
        
        disciplina = disciplina.strip()
        if not disciplina or len(disciplina) > 50:
            continue
        
        try:
            nota = float(nota)
            if 0 <= nota <= 10:
                desempenho_validado[disciplina] = nota
        except (ValueError, TypeError):
            continue
    
    if not desempenho_validado:
        raise ValidacaoErro("Pelo menos uma nota válida é necessária")
    
    return desempenho_validado

def validar_estudante(estudante: Dict[str, Any]) -> Tuple[str, List[str], List[str], Dict[str, float]]:
    """
    Valida todos os dados do estudante.
    
    Args:
        estudante: Dicionário com dados do estudante
        
    Returns:
        Tupla com (nome, interesses, habilidades, desempenho) validados
        
    Raises:
        ValidacaoErro: Se algum dado for inválido
    """
    try:
        nome = sanitizar_nome(estudante.get('nome', ''))
        interesses = validar_interesses(estudante.get('interesses', []))
        habilidades = validar_habilidades(estudante.get('habilidades', []))
        desempenho = validar_desempenho(estudante.get('desempenho', {}))
        
        return nome, interesses, habilidades, desempenho
        
    except Exception as e:
        raise ValidacaoErro(f"Erro ao validar dados do estudante: {str(e)}") 