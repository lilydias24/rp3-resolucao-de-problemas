from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Importe APENAS o router que você criou para o seu projeto
# CORREÇÃO AQUI: Certifique-se de que o nome do arquivo Python é 'project_controller.py'
from controllers.project_controller import router as project_llm_router

app = FastAPI(title="Product AI Generator API")

# Configuração de CORS: ESSENCIAL para seu React se comunicar com este backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclua APENAS o seu router
app.include_router(project_llm_router)

# Rota de teste simples (opcional, mas bom para verificar se o servidor está funcionando)
@app.get("/")
async def root():
    return {"message": "Bem-vindo à API do Gerador de Produtos AI!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)