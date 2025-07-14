from fastapi import APIRouter
from .product import router as product_router
from .auth import router as auth_router
from .llm import router as llm_router
from .dashboard import router as dashboard_router
from .review import router as review_router
from .backlog_generation import router as backlog_generation_router

router = APIRouter()
router.include_router(product_router)
router.include_router(auth_router)
router.include_router(llm_router)
router.include_router(dashboard_router)
router.include_router(review_router)
router.include_router(backlog_generation_router)


__all__ = ['router']  # Centraliza todas as rotas