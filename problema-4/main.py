from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from src.config.logging_config import setup_logging
from src.db import init_db
from src.routers import router
from contextlib import asynccontextmanager
import uvicorn
import sys
import typer

"""
Ponto de entrada da API FastAPI para o sistema de gerenciamento de histórias de usuário com LLMs.
Configura logging, CORS, lifespan, rotas e aspectos transversais (AOP).
"""
# Configuração inicial
setup_logging()
init_db()  # Cria tabelas se não existirem

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação FastAPI, logando o início da API.
    """
    logging.info("API iniciada com sucesso")
    yield
    logging.info("API finalizada")

app = FastAPI(
    title="Sistema de Gerenciamento de Histórias",
    description="API para geração e gestão de histórias de usuário com LLMs",
    version="0.1.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],  # Adicionando a porta 3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui todas as rotas definidas em src/routers/__init__.py
app.include_router(router)

@app.get("/")
async def root():
    """
    Endpoint de health check da API.
    Retorna mensagem de status e links para documentação.
    """
    return {
        "message": "API operacional",
        "docs": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        # Executar CLI
        from cli import app as cli_app
        cli_app()
    else:
        # Executar API
        print("Iniciando API FastAPI...")
        print("Para usar o CLI, execute: python main.py cli")
        print("Para acessar a documentação: http://localhost:8000/docs")
        uvicorn.run(app, host="0.0.0.0", port=8000)