from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from aspectlib import weave
from src.db.models import Product, User
from src.schemas.product import ProductCreate, ProductInDB  # Atualizado para ProductInDB
from src.db.session import get_db
from src.routers.auth import get_current_user

# Importações de aspectos
from src.aspects.logging import log_operations
from src.aspects.error_handling import handle_errors

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={
        status.HTTP_403_FORBIDDEN: {"description": "Acesso negado"},
        status.HTTP_404_NOT_FOUND: {"description": "Produto não encontrado"}
    }
)

@router.post(
    "/",
    response_model=ProductInDB,  # Schema de resposta atualizado
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Produto criado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "product_id": 1,
                        "name": "Meu Produto",
                        "description": "Descrição do produto",
                        "platforms": ["web", "mobile"],
                        "created_by": 123,
                        "created_at": "2023-11-21T10:00:00Z"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Dados inválidos ou produto já existe"
        }
    }
)

def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cria um novo produto com os dados fornecidos.
    
    - **name**: Nome do produto (deve conter espaços)
    - **description**: Descrição opcional
    - **valueProposition**: Proposta de valor (opcional)
    - **platforms**: Lista de plataformas (padrão: ["web"])
    """
    # Verifica se o produto já existe
    existing_product = db.query(Product).filter(
        Product.name == product_data.name,
        Product.created_by == current_user.user_id
    ).first()
    
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você já tem um produto com este nome"
        )

    # Criação do produto
    new_product = Product(
        **product_data.model_dump(exclude_unset=True),  # Pega apenas os campos fornecidos
        created_by=current_user.user_id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product  # Será automaticamente convertido para ProductInDB

# TODO: Implementar endpoints para épicos, histórias, requisitos, backlog, etc. no futuro.