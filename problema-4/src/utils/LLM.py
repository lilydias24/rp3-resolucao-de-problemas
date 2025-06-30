"""
Módulo utilitário para interação com a API Groq LLM, incluindo funções para resposta simples e estruturada.
"""
import os
import instructor

from groq import Groq
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

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
                "content": "Me gere histórias de usuário sobre" + content,
            }
        ],
    )
    print(resp.choices[0].message.content)
    # respJSON(content) # If you want to save the response in JSON format, uncomment this line

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




