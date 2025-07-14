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
        
        # Usar a função LLM real
        LLM(prompt)
        
        # Por enquanto, retornar um exemplo estruturado
        content = f"""Épico 1: Definição da Arquitetura do Sistema
Descrição: Estabelecer a arquitetura técnica base do sistema, incluindo escolha de tecnologias, padrões de design e estrutura de dados.

Épico 2: Implementação do Sistema de Autenticação
Descrição: Desenvolver sistema completo de autenticação e autorização de usuários com diferentes níveis de acesso.

Épico 3: Interface do Usuário Principal
Descrição: Criar interface principal do sistema com navegação intuitiva e responsiva para diferentes dispositivos.

Épico 4: Sistema de Geração de Conteúdo
Descrição: Implementar funcionalidades de geração automática de conteúdo usando IA e LLMs.

Épico 5: Gestão de Projetos e Backlog
Descrição: Desenvolver sistema completo de gestão de projetos, épicos, histórias e backlog."""
        
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
        
        # Usar a função LLM real
        LLM(prompt)
        
        # Por enquanto, retornar um exemplo estruturado
        content = f"""Como Product Owner, eu quero definir épicos claros para que a equipe tenha visão macro do projeto.

Como Desenvolvedor, eu quero acessar especificações técnicas detalhadas para que possa implementar funcionalidades corretamente.

Como Scrum Master, eu quero visualizar o backlog organizado para que possa facilitar o planejamento das sprints.

Como QA Tester, eu quero critérios de aceitação claros para que possa criar testes efetivos.

Como Stakeholder, eu quero acompanhar o progresso do projeto para que possa tomar decisões informadas."""
        
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
        
        # Por enquanto, retornar um exemplo estruturado
        content = [
            {
                "id": "REQ-001",
                "descricao": "O sistema deve permitir autenticação de usuários via email e senha",
                "prioridade": "Alta"
            },
            {
                "id": "REQ-002", 
                "descricao": "O sistema deve gerar épicos automaticamente baseado em informações do produto",
                "prioridade": "Alta"
            },
            {
                "id": "REQ-003",
                "descricao": "O sistema deve permitir edição e revisão de histórias de usuário",
                "prioridade": "Média"
            },
            {
                "id": "REQ-004",
                "descricao": "O sistema deve exportar relatórios em formato CSV e JSON",
                "prioridade": "Baixa"
            }
        ]
        
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