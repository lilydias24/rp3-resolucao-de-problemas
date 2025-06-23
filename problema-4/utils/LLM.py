import os
import instructor
import json
import re

from groq import Groq
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

from epics import Epic, print_epics

load_dotenv()



def LLM(content):
    """
    Function to interact with the API of Groq LLM and get a response based on the provided content by the user
    
    Parameters:
        content: The content that will be used with LLM to generate responses.
    """
    

        
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    
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
    # respJSON(content) // If you want to save the response in JSON format, uncomment this line

def respJSON(content):
    """function to interact with the API of Groq LLM and get a response based on the provided content by the user 
    following the structure provide in class responseStyle.

   Parameters:
        content: The content that will be used with LLM to generate responses.
    Class: 
        responseStyle: Class to define the structure of the response from the LLM for get easier to save in JSON after.
        It includes fields for name, description, and a list of facts.
    """
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )    
    class responseStyle(BaseModel):
        """
        Class to define the structure of the response from the LLM for get easier to save in JSON after.
        It includes fields for name, description, and a list of facts.
        """
        name: str = Field(..., description="The name of something or someone")
        description: str = Field(..., description="A description of the character")
        fact: List[str] = Field(..., description="A list of facts about the subject")
        
    client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)
    respJSON = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        response_model=responseStyle,
    )
    respJSON = respJSON.model_dump_json(indent=2)
    print(respJSON)



def extract_json_from_response(content):
    # remove blocos de codigo md
    content = content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
    # encontra o primeiro [ e o ultimo ]
    match = re.search(r"\\[.*\\]", content, re.DOTALL)
    if match:
        return match.group(0)
    # se nao encontrar, tenta do primeiro [ ate o ultimo ]
    start = content.find("[")
    end = content.rfind("]")
    if start != -1 and end != -1:
        return content[start:end+1]
    return content  # fallback

def generate_epics_with_llm(product_info: dict):
    """
    Usa a LLM groq para gerar épicos a partir das informações do produto.
    Retorna uma lista de objetos espic.
    """
    
    prompt = f"""
    Considere o seguinte produto:
    Nome: {product_info.get('nome', '')}
    Descrição: {product_info.get('descricao', '')}
    Personas: {', '.join(product_info.get('personas', []))}
    Proposta de valor: {product_info.get('proposta_valor', '')}

    Gere uma lista de épicos (título e descrição) para esse produto, em formato JSON.
    Exemplo de resposta:
    [
      {{"title": "Título do épico", "description": "Descrição do épico"}},
      ...
    ]
    """

    # chama o groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama3-8b-8192",  # ou o modelo que estiver sendo usado
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.2
    )
    # extrai txt da resposta
    content = response.choices[0].message.content.strip()
    json_str = extract_json_from_response(content)

    # tentar converter a resposta em json
    try:
        epics_json = json.loads(json_str)
        epics = [Epic(e['title'], e['description']) for e in epics_json]
        return epics
    except Exception as e:
        print("Erro ao processar resposta da LLM:", e)
        print("Resposta recebida:", content)
        return []




