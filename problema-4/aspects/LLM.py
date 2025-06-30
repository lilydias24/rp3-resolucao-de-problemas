import os
import json
import re
from groq import Groq
from dotenv import load_dotenv
from functools import wraps
from utils.epics import Epic

load_dotenv()

def extract_json_from_response(content):
    # remove blocos de cod markdown
    content = content.strip()
    if "```" in content:
        matches = re.findall(r"```(?:json)?\s*([\s\S]*?)```", content)
        if matches:
            content = "\n".join(matches).strip()
        else:
            content = content.replace("```json", "").replace("```", "").strip()
    # acha o primeiro [ e o ultimo ]
    start = content.find("[")
    end = content.rfind("]")
    if start != -1 and end != -1:
        json_str = content[start:end+1]
        # tenta corrigir o json cortado removendo o ultimo item que ta incompleto
        try:
            json.loads(json_str)
            return json_str
        except Exception:
            # remove o ultimo item e tenta de novo
            last_comma = json_str[:end].rfind("},")
            if last_comma != -1:
                json_str = json_str[:last_comma+1] + "]"
                try:
                    json.loads(json_str)
                    return json_str
                except Exception:
                    pass
        return json_str
    return content  # fallback

def llm_aspect(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        prompt = func(*args, **kwargs)
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        resp = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.2
        )
        content = resp.choices[0].message.content.strip()
        json_str = extract_json_from_response(content)
        try:
            epics_json = json.loads(json_str)
            epics = [Epic(e['title'], e['description']) for e in epics_json]
            return epics
        except Exception as e:
            print("Erro ao processar resposta da LLM:", e)
            print("Resposta recebida:", content)
            return []
    return wrapper

@llm_aspect
def generate_epics_with_llm(product_info: dict):
    prompt = f"""
    Considere o seguinte produto:
    Nome: {product_info.get('nome', '')}
    Descrição: {product_info.get('descricao', '')}
    Personas: {', '.join(product_info.get('personas', []))}
    Proposta de valor: {product_info.get('proposta_valor', '')}

    Gere no máximo 5 épicos (título e descrição) para esse produto, em formato JSON.
    Exemplo de resposta:
    [
      {{"title": "Título do épico", "description": "Descrição do épico"}},
      ...
    ]
    """
    return prompt

@llm_aspect
def gerar_historia_usuario(content):
    prompt = f"Me gere histórias de usuário sobre {content} sem markdown, apenas texto puro e enumeradas."
    return prompt 