from fastapi import APIRouter
from .product import router as product_router
from .auth import router as auth_router

router = APIRouter()
router.include_router(product_router)
router.include_router(auth_router)

__all__ = ['router']  # Centraliza todas as rotas