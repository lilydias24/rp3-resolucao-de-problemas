import os
import json
import re
from groq import Groq
from dotenv import load_dotenv
from functools import wraps
from src.utils.epics import Epic

load_dotenv()

def extract_json_from_response(content):
    # Remove blocos de código markdown
    content = content.strip()
    if "```" in content:
        matches = re.findall(r"```(?:json)?\s*([\s\S]*?)```", content)
        if matches:
            content = "\n".join(matches).strip()
        else:
            content = content.replace("```json", "").replace("```", "").strip()
    
    start = content.find("[")
    end = content.rfind("]")
    if start != -1 and end != -1:
        json_str = content[start:end+1]
        try:
            json.loads(json_str)
            return json_str
        except json.JSONDecodeError:
            # Tenta corrigir JSON incompleto
            last_comma = json_str.rfind("},")
            if last_comma != -1:
                corrected_json = json_str[:last_comma+1] + "]"
                try:
                    json.loads(corrected_json)
                    return corrected_json
                except json.JSONDecodeError:
                    pass # Se ainda falhar, retorna o original
        return json_str # Retorna o JSON extraído mesmo que inválido
    return content  # Fallback

def llm_aspect(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        prompt = func(*args, **kwargs)
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        resp = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um assistente especializado em Product Management. IMPORTANTE: Sempre responda em PORTUGUÊS BRASILEIRO. Nunca use inglês em suas respostas."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048,
            temperature=0.2
        )
        content = resp.choices[0].message.content.strip()
        json_str = extract_json_from_response(content)
        try:
            epics_json = json.loads(json_str)
            epics = [Epic(e.get('title', ''), e.get('description', '')) for e in epics_json]
            return epics
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Erro ao processar resposta da LLM: {e}")
            print("Resposta recebida:", content)
            # Tenta fazer um parsing mais simples se o JSON falhar
            titles = re.findall(r'"title":\s*"([^"]+)"', content)
            descriptions = re.findall(r'"description":\s*"([^"]+)"', content)
            epics = [Epic(title, desc) for title, desc in zip(titles, descriptions)]
            return epics if epics else [Epic("Erro de Geração", content)]

    return wrapper

@llm_aspect
def generate_epics_with_llm(product_info: dict):
    prompt = f"""
        IMPORTANTE: Gere todo o conteúdo em PORTUGUÊS BRASILEIRO.
        
        Considere o seguinte produto:
        Nome: {product_info.get('nome', '')}
        Descrição: {product_info.get('descricao', '')}
        Personas: {', '.join(product_info.get('personas', []))}
        Proposta de valor: {product_info.get('proposta_valor', '')}

        Gere 5 épicos (título e descrição) para esse produto, em formato JSON.
        IMPORTANTE: Todos os títulos e descrições devem estar em PORTUGUÊS BRASILEIRO.
        
        Exemplo de resposta:
        [
            {{"title": "Título do épico 1", "description": "Descrição do épico 1"}},
            {{"title": "Título do épico 2", "description": "Descrição do épico 2"}}
        ]
    """
    return prompt

@llm_aspect
def generate_user_stories_with_llm(epics: str, custom_prompt: str = None):
    prompt = f"""
        IMPORTANTE: Gere todo o conteúdo em PORTUGUÊS BRASILEIRO.
        
        Considerando os seguintes épicos:
        {epics}
        
        Gere 2 histórias de usuário para cada épico, em formato JSON.
        Exiba apenas o título e a descrição de cada história.
        IMPORTANTE: Todos os títulos e descrições devem estar em PORTUGUÊS BRASILEIRO.
        {custom_prompt or ''}
        
        Exemplo de resposta:
        [
            {{"title": "Como [persona], quero [ação], para que [benefício]", "description": "Detalhes da história."}},
            ...
        ]
    """
    return prompt

@llm_aspect
def generate_requirements_with_llm(story_title: str, story_description: str):
    prompt = f"""
        IMPORTANTE: Gere todo o conteúdo em PORTUGUÊS BRASILEIRO.
        
        Baseado na seguinte história de usuário:
        Título: {story_title}
        Descrição: {story_description}
        
        Gere 3 requisitos funcionais detalhados em formato JSON.
        IMPORTANTE: Todos os títulos e descrições devem estar em PORTUGUÊS BRASILEIRO.
        
        Exemplo de resposta:
        [
            {{"title": "Requisito 1", "description": "O sistema deve..."}},
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