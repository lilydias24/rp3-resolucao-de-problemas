import os
from groq import Groq
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

def llm_aspect(func):
    """
    Decorator para aplicar a chamada à LLM como aspecto transversal.
    A função decorada deve retornar o conteúdo a ser enviado à LLM.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        content = func(*args, **kwargs)
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
        )
        print(resp.choices[0].message.content)
        return resp.choices[0].message.content
    return wrapper

@llm_aspect
def gerar_historia_usuario(content):
    return "Me gere histórias de usuário sobre " + content + " sem markdown, apenas texto puro e enumeradas."