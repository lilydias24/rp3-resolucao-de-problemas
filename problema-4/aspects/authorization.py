import aspectlib
from fastapi import HTTPException

def require_role(role):
    """
    Cria um aspecto de autorização que restringe o acesso ao endpoint para usuários com o papel especificado.
    Exemplo: weave(endpoint, require_role('admin'))
    """
    @aspectlib.Aspect
    def aspect(cutpoint, *args, **kwargs):
        """
        Aspecto que verifica se o usuário autenticado possui o papel exigido.
        Lança HTTP 403 se não autorizado.
        """
        user = kwargs.get('current_user')
        if not user or getattr(user, 'role', None) != role:
            raise HTTPException(status_code=403, detail="Acesso negado")
        result = yield
        return result
    return aspect 