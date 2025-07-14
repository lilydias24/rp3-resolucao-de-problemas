import os
import json
import re
from groq import Groq
from dotenv import load_dotenv
from functools import wraps
from src.utils.epics import Epic

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
def generate_epics_with_llm(product_info: dict, custom_prompt: str = None):
    if custom_prompt and custom_prompt.strip():
        prompt = custom_prompt
    else:
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
def generate_user_stories_with_llm(epics: str, custom_prompt: str = None):
    if custom_prompt and custom_prompt.strip():
        prompt = custom_prompt
    else:
        prompt = f"""
                    Considerando os seguintes épicos:
                    {epics} Gere histórias de usuário para cada um deles, em formato JSON.
                    Exiba apenas o título e a descrição de cada história de usuário.
                    Exemplo de resposta:
                    [
                    {{"title": "Título da história de usuário", "description": "Descrição da história de usuário"}},
                    ...
                    ]
                """
    return prompt

def log_llm_interaction(db, user_id, product_id, prompt, response, model_used, tokens_used=None, entity_type=None, entity_id=None):
    from src.db.models import LLMInteraction
    from datetime import datetime
    interaction = LLMInteraction(
        user_id=user_id,
        product_id=product_id,
        prompt=prompt,
        response=response,
        model_used=model_used,
        tokens_used=tokens_used,
        entity_type=entity_type,
        entity_id=entity_id,
        created_at=datetime.now()
    )
    db.add(interaction)
    db.commit()
