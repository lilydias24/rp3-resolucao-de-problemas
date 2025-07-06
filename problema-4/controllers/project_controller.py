from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import json

from aspects.llm_aspects import (
    gerar_epicos_prompt, # Função para gerar épicos via aspecto
    gerar_historia_usuario_prompt, # Função para gerar histórias via aspecto
    gerar_requisitos_prompt # Função para gerar requisitos via aspecto
)

from models.llm_service import Requirement, RequirementsList # Importa as classes de esquema

router = APIRouter(
    prefix="/llm-project",
    tags=["LLM Project Generation"],
)

# Modelos Pydantic para os dados de entrada das requisições (permanecem os mesmos)
class ProductInfo(BaseModel):
    nome: str
    descricao: str
    personas: str
    proposta: str
    canais: str

class GenerateEpicsRequest(BaseModel):
    productInfo: str

class GenerateUserStoriesRequest(BaseModel):
    productInfo: str
    epicsSummary: str
    userPromptAdjustment: str = ""

class GenerateRequirementsRequest(BaseModel):
    userStories: str
    productInfo: str

@router.post("/generate-epics")
async def generate_epics(request_body: GenerateEpicsRequest):
    """
    Gera épicos de projeto usando a LLM com base nas informações do produto, usando o aspecto.
    """
    print("\n--- Requisição POST /llm-project/generate-epics recebida! ---")
    print(f"Corpo da requisição para épicos: {request_body.model_dump_json(indent=2)}")

    product_info = request_body.productInfo
    if not product_info:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Informações do produto são necessárias para gerar épicos.")

    try:
        epics_content = gerar_epicos_prompt(product_info=product_info)
        print("Aspecto retornou conteúdo para épicos.")
        return {"content": epics_content}
    except RuntimeError as e:
        print(f"Erro RuntimeError no aspecto ao gerar épicos: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Falha ao gerar épicos: {e}")
    except Exception as e:
        print(f"Erro Exception genérica ao gerar épicos: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro inesperado ao gerar épicos: {e}")

@router.post("/generate-user-stories")
async def generate_user_stories(request_body: GenerateUserStoriesRequest):
    """
    Gera histórias de usuário usando a LLM com base nas informações do produto e épicos, usando o aspecto.
    """
    print("\n--- Requisição POST /llm-project/generate-user-stories recebida! ---")
    print(f"Corpo da requisição para histórias: {request_body.model_dump_json(indent=2)}")

    product_info = request_body.productInfo
    epics_summary = request_body.epicsSummary
    user_prompt_adjustment = request_body.userPromptAdjustment

    if not product_info or not epics_summary:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Informações do produto e épicos são necessárias para gerar histórias.")

    try:
        user_stories_content = gerar_historia_usuario_prompt(
            product_info=product_info,
            epics_summary=epics_summary,
            user_prompt_adjustment=user_prompt_adjustment
        )
        print("Aspecto retornou conteúdo para histórias de usuário.")
        return {"content": user_stories_content}
    except RuntimeError as e:
        print(f"Erro RuntimeError no aspecto ao gerar histórias: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Falha ao gerar histórias de usuário: {e}")
    except Exception as e:
        print(f"Erro Exception genérica ao gerar histórias: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro inesperado ao gerar histórias de usuário: {e}")

@router.post("/generate-requirements")
async def generate_requirements(request_body: GenerateRequirementsRequest):
    """
    Gera requisitos funcionais usando a LLM com base nas histórias de usuário, esperando uma saída JSON.
    """
    print("\n--- Requisição POST /llm-project/generate-requirements recebida! ---")
    print(f"Corpo da requisição para requisitos: {request_body.model_dump_json(indent=2)}")

    user_stories = request_body.userStories
    product_info = request_body.productInfo

    if not user_stories:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Histórias de usuário são necessárias para gerar requisitos.")

    try:
        requirements_content = gerar_requisitos_prompt(
            user_stories=user_stories,
            product_info=product_info
        )
        print("Aspecto retornou conteúdo para requisitos.")

        # Tentar carregar como JSON
        try:
            # Remover possíveis blocos de código markdown se a LLM os incluir acidentalmente
            if requirements_content.strip().startswith('```json') and requirements_content.strip().endswith('```'):
                requirements_content = requirements_content.strip()[len('```json'):-len('```')].strip()

            parsed_requirements = json.loads(requirements_content)
            # Retorne o JSON parseado dentro da chave 'content' para consistência com os outros endpoints
            return {"content": parsed_requirements}
        except json.JSONDecodeError as json_err:
            print(f"ERRO CRÍTICO: LLM não retornou JSON válido para requisitos: {json_err}. Conteúdo problemático: {requirements_content[:500]}...")
            # Em caso de erro na decodificação JSON, retorne uma mensagem clara e o texto bruto se necessário para depuração
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Falha na análise JSON dos requisitos gerados: {json_err}. Tente novamente ou ajuste o prompt. Conteúdo bruto (parcial): {requirements_content[:200]}"
            )

    except RuntimeError as e:
        print(f"Erro RuntimeError no aspecto ao gerar requisitos: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Falha ao gerar requisitos: {e}")
    except Exception as e:
        print(f"Erro Exception genérica ao gerar requisitos: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro inesperado ao gerar requisitos: {e}")
