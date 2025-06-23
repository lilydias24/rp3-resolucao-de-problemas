from fastapi import APIRouter

router = APIRouter()

@router.get("/login")
def login():
    """
    Endpoint de exemplo para login.
    Retorna uma mensagem simples indicando o endpoint de login.
    """
    return {"message": "Endpoint de login (exemplo)"} 