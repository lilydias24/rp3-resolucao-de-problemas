# backend/aspects/llm_aspects.py

import os
from groq import Groq
from dotenv import load_dotenv
from functools import wraps

load_dotenv() # Garanta que o .env seja carregado no nível do módulo

def llm_aspect(func):
    """
    Decorator para aplicar a chamada à LLM como aspecto transversal (para TEXTO LIVRE).
    A função decorada deve retornar o conteúdo (prompt) a ser enviado à LLM.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        prompt_content = func(*args, **kwargs) # A função decorada (ex: gerar_epicos_prompt) gera o prompt

        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            # Isso vai aparecer no terminal do FastAPI se a chave não for encontrada
            raise ValueError("GROQ_API_KEY não configurada nas variáveis de ambiente.")

        client = Groq(api_key=api_key)

        try:
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile", # Verifique o modelo mais recente disponível no Groq
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um assistente especialista em Product Management. Gere conteúdo de forma clara, concisa e útil.",
                    },
                    {
                        "role": "user",
                        "content": prompt_content,
                    }
                ],
                temperature=0.7, # Adicionado para consistência na chamada
                max_tokens=1500, # Adicionado para limitar o tamanho da resposta
            )
            generated_content = resp.choices[0].message.content
            print(f"LLM Aspect: Conteúdo gerado pela LLM para '{func.__name__}':\n{generated_content[:500]}...") # Log para depuração
            return generated_content
        except Exception as e:
            print(f"LLM Aspect: Erro na chamada da API Groq para '{func.__name__}': {e}")
            raise RuntimeError(f"Falha ao se comunicar com a LLM via aspecto: {str(e)}")
    return wrapper

@llm_aspect
def gerar_epicos_prompt(product_info: str):
    """Retorna o prompt para a LLM para criar épicos. A chamada à LLM é feita pelo llm_aspect."""
    return f"Gere uma hierarquia de Épicos para um novo projeto de software baseado nas seguintes informações do produto:\n\n{product_info}\n\nPara cada épico, inclua o nome e uma breve descrição."

@llm_aspect
def gerar_historia_usuario_prompt(product_info: str, epics_summary: str, user_prompt_adjustment: str = ""):
    """Retorna o prompt para a LLM para criar histórias de usuário. A chamada à LLM é feita pelo llm_aspect."""
    base_prompt = f"Com base no produto:\n{product_info}\n\nE nos épicos:\n{epics_summary}\n\n Gere um conjunto de histórias de usuário detalhadas, no formato 'Como <persona>, quero <ação>, para que <benefício>'. Priorize as histórias (Alto, Médio, Baixo)."
    final_prompt = base_prompt
    if user_prompt_adjustment:
        final_prompt += f"\n\nAlém disso, considere o seguinte ajuste no prompt: {user_prompt_adjustment}"
    return final_prompt

@llm_aspect
def gerar_requisitos_prompt(user_stories: str, product_info: str):
    """Retorna o prompt para a LLM para criar requisitos funcionais. A chamada à LLM é feita pelo llm_aspect."""
    # ATENÇÃO: Este aspecto retorna TEXTO PURO. Se precisar de JSON estruturado,
    # o aspecto 'llm_aspect' precisaria ser modificado para usar 'instructor' e 'response_model',
    # ou você criaria um segundo aspecto específico para isso.
    return f"Com base nas seguintes histórias de usuário:\n\n{user_stories}\n\nE no produto com informações: {product_info}\n\n Gere uma lista de requisitos funcionais detalhados, cada um com um ID único, uma descrição clara e sua prioridade (Alta, Média, Baixa). Retorne apenas o texto dos requisitos, sem formatação de código JSON."