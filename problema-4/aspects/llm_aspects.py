import os
from groq import Groq
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

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
                        "content": (
                            "Você é uma inteligência artificial que simula as funcionalidades de um sistema de Product"
                            "Management. Seu objetivo é me ajudar a gerar artefatos de produto. Para cada solicitação,"
                            "eu fornecerei o contexto necessário. Gere o conteúdo de forma clara, concisa e útil, sem"
                            "markdown, e escreva apenas o que foi solicitado. Não inclua explicações ou justificativas."
                        ),
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
    return (
        f"Gere uma hierarquia de 10 Épicos para um novo projeto de software. "
        f"Baseie-se nas seguintes informações do produto:\n\n{product_info}\n\n"
        f"Para cada épico, forneça apenas a numeração, o 'Nome do Épico' e, em seguida, uma 'Breve Descrição'. "
        f"Não inclua introduções, encerramentos ou qualquer texto adicional além dos épicos solicitados."
    )

@llm_aspect
def gerar_historia_usuario_prompt(product_info: str, epics_summary: str, user_prompt_adjustment: str = ""):
    """Retorna o prompt para a LLM para criar histórias de usuário. A chamada à LLM é feita pelo llm_aspect."""
    base_prompt = (
        f"Gere um conjunto de histórias de usuário detalhadas. "
        f"Use as seguintes informações do produto:\n{product_info}\n\n"
        f"E os seguintes Épicos para contextualização:\n{epics_summary}\n\n"
        f"Para cada história, utilize o formato exato: 'Como <persona>, quero <ação>, para que <benefício>'. "
        f"Após a história, indique a prioridade: 'Prioridade: [Alto/Médio/Baixo]'. "
        f"Não adicione introduções, encerramentos, numeração ou qualquer texto extra."
        f"Em cada história adicione o número do épico relacionado. Como exemplo: ( 1. Nome do Épico )\n\n"
    )
    
    final_prompt = base_prompt
    if user_prompt_adjustment:
        final_prompt += f"\n\nConsidere também o seguinte ajuste adicional para a geração: {user_prompt_adjustment}"
    return final_prompt

@llm_aspect
def gerar_requisitos_prompt(user_stories: str, product_info: str):
    # Não está sendo usado ainda porque não sei como funcionará para integrar com o banco o que será salvo
    """Retorna o prompt para a LLM para criar requisitos funcionais. A chamada à LLM é feita pelo llm_aspect."""
    return (
        f"Com base nas seguintes histórias de usuário:\n\n{user_stories}\n\nE no produto com informações: "
        f" {product_info}\n\n Gere uma lista de requisitos funcionais detalhados, cada um com um ID único, uma "
        f" descrição clara e sua prioridade (Alta, Média, Baixa). Retorne apenas o texto dos requisitos, sem "
        f" formatação de código JSON."
    )