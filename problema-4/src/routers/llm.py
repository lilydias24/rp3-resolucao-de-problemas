import logging
from fastapi import APIRouter, HTTPException, status
from src.schemas.llm import LLMRequest, LLMResponse
from src.utils.LLM import LLM
from aspects.logging import logging_aspect
from aspects.error_handling import handle_errors
from aspects.notification import notification_aspect

router = APIRouter(
    prefix="/llm-project",
    tags=["llm"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Erro interno do servidor"}
    }
)

@router.post("/generate-epics", response_model=LLMResponse)
@handle_errors
@logging_aspect
@notification_aspect
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
        
        # Usar o aspecto LLM para gerar épicos
        from aspects.llm_aspects import gerar_epicos_prompt
        try:
            logging.info(f"Chamando gerar_epicos_prompt com product_info: {request.productInfo}")
            content = gerar_epicos_prompt(product_info=request.productInfo)
            logging.info(f"Conteúdo gerado: {content[:200]}...")
        except Exception as e:
            logging.error(f"Erro ao chamar gerar_epicos_prompt: {str(e)}")
            raise
        
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
@handle_errors
@logging_aspect
@notification_aspect
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
        
        # Usar o aspecto LLM para gerar histórias de usuário
        from aspects.llm_aspects import gerar_historia_usuario_prompt
        if not request.epicsSummary:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resumo dos épicos é necessário para gerar histórias de usuário.")
        content = gerar_historia_usuario_prompt(
            product_info=request.productInfo,
            epics_summary=request.epicsSummary,
            user_prompt_adjustment=request.userPromptAdjustment or ""
        )
        
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
@handle_errors
@logging_aspect
@notification_aspect
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
        
        # Usar a função LLM real
        LLM(prompt)
        
        # Usar o aspecto LLM para gerar requisitos
        from aspects.llm_aspects import gerar_requisitos_prompt
        if not request.userStories:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Histórias de usuário são necessárias para gerar requisitos.")
        content = gerar_requisitos_prompt(user_stories=request.userStories, product_info=request.productInfo)
        
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