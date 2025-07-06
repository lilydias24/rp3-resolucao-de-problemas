from fastapi import APIRouter, HTTPException, status
from src.schemas.llm import LLMRequest, LLMResponse
from src.utils.LLM import LLM
import logging

router = APIRouter(
    prefix="/llm-project",
    tags=["llm"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Erro interno do servidor"}
    }
)

@router.post("/generate-epics", response_model=LLMResponse)
async def generate_epics(request: LLMRequest):
    """
    Gera épicos baseados nas informações do produto
    """
    try:
        prompt = f"""
        Com base nas seguintes informações do produto, gere uma lista detalhada de épicos:
        
        {request.productInfo}
        
        {request.userPromptAdjustment or ''}
        
        Por favor, gere épicos bem estruturados e organizados.
        """
        
        # Aqui você precisará modificar a função LLM para retornar o conteúdo
        # Por enquanto, vou criar uma versão que retorna o prompt
        content = f"Épicos gerados para: {request.productInfo}"
        
        return LLMResponse(
            content=content,
            success=True,
            message="Épicos gerados com sucesso"
        )
    except Exception as e:
        logging.error(f"Erro ao gerar épicos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar épicos: {str(e)}"
        )

@router.post("/generate-user-stories", response_model=LLMResponse)
async def generate_user_stories(request: LLMRequest):
    """
    Gera histórias de usuário baseadas nos épicos
    """
    try:
        prompt = f"""
        Com base nas seguintes informações, gere histórias de usuário detalhadas:
        
        Informações do Produto: {request.productInfo}
        Épicos: {request.epicsSummary or 'Não fornecidos'}
        
        {request.userPromptAdjustment or ''}
        
        Por favor, gere histórias de usuário bem estruturadas seguindo o formato: "Como [persona], eu quero [objetivo] para que [benefício]"
        """
        
        content = f"Histórias de usuário geradas para: {request.productInfo}"
        
        return LLMResponse(
            content=content,
            success=True,
            message="Histórias de usuário geradas com sucesso"
        )
    except Exception as e:
        logging.error(f"Erro ao gerar histórias de usuário: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar histórias de usuário: {str(e)}"
        )

@router.post("/generate-requirements", response_model=LLMResponse)
async def generate_requirements(request: LLMRequest):
    """
    Gera requisitos funcionais baseados nas histórias de usuário
    """
    try:
        prompt = f"""
        Com base nas seguintes informações, gere requisitos funcionais detalhados:
        
        Informações do Produto: {request.productInfo}
        Histórias de Usuário: {request.userStories or 'Não fornecidas'}
        
        {request.userPromptAdjustment or ''}
        
        Por favor, gere requisitos funcionais bem estruturados e organizados.
        """
        
        content = f"Requisitos funcionais gerados para: {request.productInfo}"
        
        return LLMResponse(
            content=content,
            success=True,
            message="Requisitos funcionais gerados com sucesso"
        )
    except Exception as e:
        logging.error(f"Erro ao gerar requisitos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar requisitos: {str(e)}"
        )