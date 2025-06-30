from aspectlib import Aspect
from fastapi import HTTPException
import aspectlib

@aspectlib.Aspect
def handle_errors(cutpoint, *args, **kwargs):
    """
    Aspecto para capturar e tratar exceções, convertendo-as em HTTPException apropriadas para FastAPI.
    - HTTPException: propagada normalmente
    - Outras exceções: viram HTTP 500
    """
    try:
        result = yield
        return result
    except HTTPException:
        raise  # Deixa HTTPException passar normalmente
    except Exception as e:
        # Loga o erro se quiser
        raise HTTPException(status_code=500, detail="Erro interno") from e