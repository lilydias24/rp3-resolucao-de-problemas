from functools import wraps
from fastapi import HTTPException, status

def require_role(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Try to get user from kwargs first, then from args
            user = kwargs.get('current_user')
            if user is None and len(args) > 2:
                user = args[2]
            
            # Check if user exists and has the required role
            if user is None:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário não autenticado")
            
            if getattr(user, 'role', None) != role:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado - papel insuficiente")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def require_admin(func):
    """
    Decorator que requer papel de admin para executar a função.
    """
    return require_role('admin')(func) 