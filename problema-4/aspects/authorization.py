from functools import wraps
from fastapi import HTTPException, status

def require_role(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get('current_user') or (args[2] if len(args) > 2 else None)
            if not user or getattr(user, 'role', None) != role:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")
            return func(*args, **kwargs)
        return wrapper
    return decorator 