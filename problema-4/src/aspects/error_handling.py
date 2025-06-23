from aspectlib import Aspect
from fastapi import HTTPException

@Aspect
def handle_errors(*args, **kwargs):
    """
    Aspecto para capturar e tratar exceções, convertendo-as em HTTPException apropriadas para FastAPI.
    - ValueError vira HTTP 400
    - Outras exceções viram HTTP 500
    """
    try:
        yield
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno")