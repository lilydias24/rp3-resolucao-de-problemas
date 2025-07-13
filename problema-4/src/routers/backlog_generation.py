"""
Router para geração automática de backlog.
Inclui endpoints para gerar backlog a partir de histórias e requisitos aprovados.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.db.models import User
from src.schemas.backlog_generation import (
    BacklogGenerationRequest, BacklogGenerationResponse, BacklogGenerationPreview,
    BacklogGenerationOptions, GenerationStrategy
)
from src.utils.backlog_generator import BacklogGenerator
from src.db.session import get_db
from src.routers.auth import get_current_user
from aspects.logging import logging_aspect
from aspects.error_handling import handle_errors
from aspects.notification import notification_aspect

router = APIRouter(
    prefix="/backlog-generation",
    tags=["backlog-generation"],
    responses={
        status.HTTP_403_FORBIDDEN: {"description": "Acesso negado"},
        status.HTTP_404_NOT_FOUND: {"description": "Produto não encontrado"},
        status.HTTP_400_BAD_REQUEST: {"description": "Dados inválidos"}
    }
)

@router.post("/preview", response_model=BacklogGenerationPreview)
@handle_errors
@logging_aspect
def preview_backlog_generation(
    request: BacklogGenerationRequest,
    options: BacklogGenerationOptions = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Gera um preview da geração de backlog sem criar o backlog.
    Útil para verificar o que será gerado antes de confirmar.
    """
    try:
        generator = BacklogGenerator(db)
        preview = generator.preview_generation(request, options)
        return preview
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar preview: {str(e)}")

@router.post("/generate", response_model=BacklogGenerationResponse)
@handle_errors
@logging_aspect
@notification_aspect
def generate_backlog(
    request: BacklogGenerationRequest,
    options: BacklogGenerationOptions = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Gera um backlog automaticamente a partir de histórias e requisitos aprovados.
    """
    try:
        generator = BacklogGenerator(db)
        response = generator.generate_backlog(request, options)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar backlog: {str(e)}")

@router.post("/generate/quick", response_model=BacklogGenerationResponse)
@handle_errors
@logging_aspect
@notification_aspect
def generate_quick_backlog(
    product_id: int,
    name: str,
    description: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Gera um backlog rapidamente com configurações padrão.
    """
    try:
        request = BacklogGenerationRequest(
            product_id=product_id,
            name=name,
            description=description,
            strategy=GenerationStrategy.PRIORITY_BASED,
            include_stories=True,
            include_requirements=True,
            min_priority=3,
            auto_prioritize=True
        )
        
        options = BacklogGenerationOptions()
        
        generator = BacklogGenerator(db)
        response = generator.generate_backlog(request, options)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar backlog: {str(e)}")

@router.get("/strategies")
@handle_errors
@logging_aspect
def get_generation_strategies():
    """
    Retorna as estratégias de geração disponíveis.
    """
    strategies = [
        {
            "value": GenerationStrategy.PRIORITY_BASED,
            "name": "Baseado em Prioridade",
            "description": "Ordena itens por prioridade e outros fatores como recência e complexidade"
        },
        {
            "value": GenerationStrategy.EPIC_BASED,
            "name": "Baseado em Épicos",
            "description": "Agrupa itens por épicos e ordena por prioridade dentro de cada épico"
        },
        {
            "value": GenerationStrategy.STORY_ONLY,
            "name": "Apenas Histórias",
            "description": "Inclui apenas histórias de usuário aprovadas"
        },
        {
            "value": GenerationStrategy.REQUIREMENT_ONLY,
            "name": "Apenas Requisitos",
            "description": "Inclui apenas requisitos aprovados"
        },
        {
            "value": GenerationStrategy.MIXED,
            "name": "Misto",
            "description": "Alterna entre histórias e requisitos para balancear o backlog"
        }
    ]
    
    return {"strategies": strategies}

@router.get("/products/{product_id}/approved-items")
@handle_errors
@logging_aspect
def get_approved_items_count(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retorna a contagem de histórias e requisitos aprovados para um produto.
    Útil para verificar se há itens suficientes para gerar um backlog.
    """
    from src.db.models import Epic, UserStory, Requirement
    from src.schemas.review import ReviewStatus
    from sqlalchemy import and_
    
    # Contar histórias aprovadas
    stories_count = db.query(UserStory).join(Epic).filter(
        and_(
            Epic.product_id == product_id,
            UserStory.status == ReviewStatus.APPROVED.value
        )
    ).count()
    
    # Contar requisitos aprovados
    requirements_count = db.query(Requirement).join(UserStory).join(Epic).filter(
        and_(
            Epic.product_id == product_id,
            Requirement.status == ReviewStatus.APPROVED.value
        )
    ).count()
    
    return {
        "product_id": product_id,
        "approved_stories": stories_count,
        "approved_requirements": requirements_count,
        "total_approved_items": stories_count + requirements_count,
        "can_generate_backlog": (stories_count + requirements_count) > 0
    }

@router.get("/products/{product_id}/epics-summary")
@handle_errors
@logging_aspect
def get_epics_summary(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retorna um resumo dos épicos com suas histórias e requisitos aprovados.
    Útil para entender a distribuição de itens por épico.
    """
    from src.db.models import Epic, UserStory, Requirement
    from src.schemas.review import ReviewStatus
    from sqlalchemy import and_, func
    
    # Buscar épicos do produto
    epics = db.query(Epic).filter(Epic.product_id == product_id).all()
    
    summary = []
    for epic in epics:
        # Contar histórias aprovadas
        approved_stories = db.query(UserStory).filter(
            and_(
                UserStory.epic_id == epic.epic_id,
                UserStory.status == ReviewStatus.APPROVED.value
            )
        ).count()
        
        # Contar requisitos aprovados
        approved_requirements = db.query(Requirement).join(UserStory).filter(
            and_(
                UserStory.epic_id == epic.epic_id,
                Requirement.status == ReviewStatus.APPROVED.value
            )
        ).count()
        
        summary.append({
            "epic_id": epic.epic_id,
            "epic_title": epic.title,
            "epic_status": epic.status,
            "approved_stories": approved_stories,
            "approved_requirements": approved_requirements,
            "total_approved_items": approved_stories + approved_requirements
        })
    
    return {
        "product_id": product_id,
        "epics_summary": summary,
        "total_epics": len(summary),
        "epics_with_approved_items": len([epic for epic in summary if epic["total_approved_items"] > 0])
    } 