from aspects.LLM import generate_epics_with_llm
from src.utils.epics import print_epics

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from src.config.logging_config import setup_logging
from src.db import init_db
from src.routers import router 
from src.routers.product import create_product
from src.routers.auth import register, login
from aspectlib import weave
from aspects.logging import log_operations
from aspects.error_handling import handle_errors
from contextlib import asynccontextmanager
from aspects.authorization import require_role
from aspects.notification import notify_on_event

"""
Ponto de entrada da API FastAPI para o sistema de gerenciamento de histórias de usuário com LLMs.
Configura logging, CORS, lifespan, rotas e aspectos transversais (AOP).
"""
# Configuração inicial
setup_logging()
init_db()  # Cria tabelas se não existirem

@asynccontextmanager
async def lifespan(app):
    """
    Gerencia o ciclo de vida da aplicação FastAPI, logando o início da API.
    """
    logging.info("API iniciada com sucesso")
    yield

app = FastAPI(
    title="Sistema de Gerenciamento de Histórias",
    description="API para geração e gestão de histórias de usuário com LLMs",
    version="0.1.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
weave(create_product, notify_on_event)

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

# CLI
# def pedir_product_info():
#     """Coleta informações do produto via CLI"""
#     print("\n" + "="*50)
#     print("GERADOR DE ÉPICOS - MODO CLI")
#     print("="*50)
    
#     nome = input("Nome do produto: ")
#     descricao = input("Descrição do produto: ")
#     personas = input("Personas (separe por vírgula): ").split(",")
#     personas = [p.strip() for p in personas]
#     proposta_valor = input("Proposta de valor: ")
#     canais = input("Canais/Plataformas (opcional): ")
    
#     return {
#         "nome": nome,
#         "descricao": descricao,
#         "personas": personas,
#         "proposta_valor": proposta_valor,
#         "canais": canais
#     }

# def main():
#     """Função principal do modo CLI"""
#     while True:
#         print("\n" + "="*50)
#         print("Bem vindo PO! Escolha uma opção:")
#         print("1 - Gerar épicos para um produto (usando LLM)")
#         print("2 - Gerar épicos com prompt customizado")
#         print("0 - Sair")
#         print("="*50)
        
#         opt = input("Opção: ")
        
#         if opt == "1":
#             product_info = pedir_product_info()
#             print("\nGerando épicos...")
#             epics = generate_epics_with_llm(product_info)
#             print_epics(epics)
            
#         elif opt == "2":
#             product_info = pedir_product_info()
#             custom_prompt = input("\nPrompt customizado (deixe vazio para usar padrão): ")
            
#             if custom_prompt.strip():
#                 # aqui vai o prompt customizado, quando eu fizer
#                 print("Funcionalidade de prompt customizado vai ser implementada em breve")
#             else:
#                 print("\nGerando épicos com prompt padrão...")
#                 epics = generate_epics_with_llm(product_info)
#                 print_epics(epics)
                
#         elif opt == "0":
#             print("Saindo...")
#             break
#         else:
#             print("Opção inválida!")

# if __name__ == "__main__":
#     main()