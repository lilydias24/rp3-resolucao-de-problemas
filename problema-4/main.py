from fastapi import FastAPI
import logging
from src.config.logging_config import setup_logging
from src.db import init_db
from src.routers import router  # Importa o router consolidado
from src.routers.product import create_product
from src.routers.auth import register, login
from aspectlib import weave
from src.aspects.logging import log_operations
from src.aspects.error_handling import handle_errors
from contextlib import asynccontextmanager
from src.aspects.authorization import require_role

# Configuração inicial
setup_logging()
#init_db()  # Cria tabelas se não existirem

@asynccontextmanager
async def lifespan(app):
    logging.info("API iniciada com sucesso")
    yield

app = FastAPI(
    title="Sistema de Gerenciamento de Histórias",
    description="API para geração e gestão de histórias de usuário com LLMs",
    version="0.1.0",
    lifespan=lifespan
)

# Inclui todas as rotas definidas em src/routers/__init__.py
app.include_router(router)

# weave dos aspectos (após todos os imports)
weave(create_product, log_operations)
weave(create_product, handle_errors)
weave(register, log_operations)
weave(register, handle_errors)
weave(login, log_operations)
weave(login, handle_errors)
# Exemplo: só admin pode criar produto
weave(create_product, require_role('admin'))

@app.get("/")
async def root():
    """Endpoint health check"""
    return {
        "message": "API operacional",
        "docs": "/docs",
        "redoc": "/redoc"
    }