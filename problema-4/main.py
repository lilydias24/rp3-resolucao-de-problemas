from fastapi import FastAPI
import logging
from src.config.logging_config import setup_logging
from src.db import init_db
from src.routers import router  # Importa o router consolidado

# Configuração inicial
setup_logging()
init_db()  # Cria tabelas se não existirem

app = FastAPI(
    title="Sistema de Gerenciamento de Histórias",
    description="API para geração e gestão de histórias de usuário com LLMs",
    version="0.1.0"
)

# Inclui todas as rotas definidas em src/routers/__init__.py
app.include_router(router)

@app.on_event("startup")
async def startup():
    """Evento de inicialização da aplicação"""
    logging.info("API iniciada com sucesso")

@app.get("/")
async def root():
    """Endpoint health check"""
    return {
        "message": "API operacional",
        "docs": "/docs",
        "redoc": "/redoc"
    }