from aspects.LLM import generate_epics_with_llm, generate_user_stories_with_llm
from src.utils.epics import print_epics, print_user_stories
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from src.config.logging_config import setup_logging
from src.db import init_db
from src.routers import router 
from src.routers.product import business_create_product
from src.routers.auth import register, login
#from aspectlib import weave
from contextlib import asynccontextmanager
import uvicorn

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
def pedir_product_info():
    """Coleta informações do produto via CLI"""
    print("\n" + "="*50)
    print("GERADOR DE ÉPICOS - MODO CLI")
    print("="*50)
    
    nome = input("Nome do produto: ")
    descricao = input("Descrição do produto: ")
    personas = input("Personas (separe por vírgula): ").split(",")
    personas = [p.strip() for p in personas]
    proposta_valor = input("Proposta de valor: ")
    canais = input("Canais/Plataformas (opcional): ")
    
    return {
        "nome": nome,
        "descricao": descricao,
        "personas": personas,
        "proposta_valor": proposta_valor,
        "canais": canais
    }

def main():
    """Função principal do modo CLI"""
    while True:
        print("\n" + "="*80)
        print("\t Bem vindo PO! Escolha uma opção: \n")
        print("\t 1 - Gerar épicos para um produto (usando LLM)")
        print("\t 2 - Gerar épicos com prompt customizado")
        print("\t 0 - Sair")
        print("="*80)
        
        opt = input("Opção: ")
        
        if opt == "1":
            product_info = pedir_product_info()
            print("\nGerando épicos...")
            epics = generate_epics_with_llm(product_info)
            print_epics(epics)


            print("\n\t Deseja exibir histórias de usuário geradas ? (S/N)")
            if input().strip().lower() == 's':

                print("\t 1 - Gerar épicos para um produto (usando LLM)")
                print("\t 2 - Gerar épicos com prompt customizado")
                
                opt = input("Opção: ")
                if opt == "1":
                    print("\nGerando histórias de usuário...")
                    user_stories = generate_user_stories_with_llm(epics)
                    print_user_stories(user_stories) 
                elif opt == "2":
                    custom_prompt = input("\nPrompt customizado (deixe vazio para usar padrão): ")
                    if custom_prompt.strip():
                        print("Funcionalidade de prompt customizado vai ser implementada em breve")
                    else:
                        print("\nGerando histórias de usuário com prompt padrão...")
                        user_stories = generate_user_stories_with_llm(epics)
                        print_user_stories(user_stories)
            else:
                print("\nHistórias de usuário não serão exibidas.")
            
        elif opt == "2":
            product_info = pedir_product_info()
            custom_prompt = input("\nPrompt customizado (deixe vazio para usar padrão): ")
            
            if custom_prompt.strip():
                # aqui vai o prompt customizado, quando eu fizer
                print("Funcionalidade de prompt customizado vai ser implementada em breve")
            else:
                print("\nGerando épicos com prompt padrão...")
                epics = generate_epics_with_llm(product_info)
                print_epics(epics)
                
        elif opt == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)