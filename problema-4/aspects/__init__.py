"""
Inicializa o pacote de aspectos, expondo os principais aspectos transversais.
"""

from .error_handling import handle_errors

__all__ = ['handle_errors', 'validate_input']