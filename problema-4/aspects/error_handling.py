from fastapi import HTTPException
from functools import wraps
import traceback

def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("ERRO INTERNO:", e)
            traceback.print_exc()  # <--- Adicione esta linha
            raise HTTPException(status_code=500, detail="Erro interno")
    return wrapper