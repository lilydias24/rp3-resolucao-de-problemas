"""
Router para o sistema de revisão/sugestão.
Inclui endpoints para comentários, ações de revisão e gerenciamento de status.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.db.models import ReviewComment, ReviewStatusHistory, Epic, UserStory, Requirement, User, Backlog
from src.schemas.review import (
    ReviewCommentCreate, ReviewCommentInDB, ReviewActionRequest, 
    ReviewStatusUpdate, EntityReviewInfo, ReviewSummary, ReviewStatus, ReviewAction
)
from src.db.session import get_db
from src.routers.auth import get_current_user
from aspects.logging import logging_aspect
from aspects.error_handling import handle_errors
from aspects.notification import notification_aspect
from aspects.revision_tracking import track_revisions
from datetime import datetime

router = APIRouter(
    prefix="/review",
    tags=["review"],
    responses={
        status.HTTP_403_FORBIDDEN: {"description": "Acesso negado"},
        status.HTTP_404_NOT_FOUND: {"description": "Entidade não encontrada"}
    }
)

# --- COMENTÁRIOS DE REVISÃO ---

@router.post("/comments", response_model=ReviewCommentInDB)
@handle_errors
@logging_aspect
@notification_aspect
def create_review_comment(
    comment_data: ReviewCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cria um novo comentário de revisão para uma entidade.
    """
    # Validar se a entidade existe
    entity = _get_entity(db, comment_data.entity_type, comment_data.entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail=f"{comment_data.entity_type} não encontrado")
    
    # Criar comentário
    new_comment = ReviewComment(
        entity_type=comment_data.entity_type,
        entity_id=comment_data.entity_id,
        comment=comment_data.comment,
        is_suggestion=comment_data.is_suggestion,
        suggested_changes=comment_data.suggested_changes,
        created_by=current_user.user_id
    )
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return new_comment

@router.get("/comments/{entity_type}/{entity_id}", response_model=List[ReviewCommentInDB])
@handle_errors
@logging_aspect
def get_review_comments(
    entity_type: str,
    entity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista todos os comentários de revisão de uma entidade.
    """
    comments = db.query(ReviewComment).filter(
        ReviewComment.entity_type == entity_type,
        ReviewComment.entity_id == entity_id
    ).order_by(ReviewComment.created_at.desc()).all()
    
    return comments

@router.delete("/comments/{comment_id}", status_code=204)
@handle_errors
@logging_aspect
@notification_aspect
def delete_review_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Remove um comentário de revisão (apenas o autor pode remover).
    """
    comment = db.query(ReviewComment).filter(ReviewComment.comment_id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")
    
    if comment.created_by != current_user.user_id:
        raise HTTPException(status_code=403, detail="Apenas o autor pode remover o comentário")
    
    db.delete(comment)
    db.commit()
    return None

# --- AÇÕES DE REVISÃO ---

@router.post("/{entity_type}/{entity_id}/action")
@handle_errors
@track_revisions
@logging_aspect
@notification_aspect
def perform_review_action(
    entity_type: str,
    entity_id: int,
    action_request: ReviewActionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Executa uma ação de revisão em uma entidade (aprovar, rejeitar, etc.).
    """
    entity = _get_entity(db, entity_type, entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail=f"{entity_type} não encontrado")
    
    # Mapear ação para novo status
    status_mapping = {
        ReviewAction.SUBMIT_FOR_REVIEW: ReviewStatus.IN_REVIEW,
        ReviewAction.APPROVE: ReviewStatus.APPROVED,
        ReviewAction.REJECT: ReviewStatus.REJECTED,
        ReviewAction.REQUEST_REVISION: ReviewStatus.NEEDS_REVISION,
        ReviewAction.MARK_IMPLEMENTED: ReviewStatus.IMPLEMENTED
    }
    
    new_status = status_mapping.get(action_request.action)
    if not new_status:
        raise HTTPException(status_code=400, detail="Ação inválida")
    
    # Atualizar status da entidade
    old_status = entity.status
    entity.status = new_status.value
    entity.updated_at = datetime.utcnow()
    
    # Registrar mudança no histórico
    status_history = ReviewStatusHistory(
        entity_type=entity_type,
        entity_id=entity_id,
        old_status=old_status,
        new_status=new_status.value,
        changed_by=current_user.user_id,
        reason=action_request.reason
    )
    
    db.add(status_history)
    
    # Adicionar comentário se fornecido
    if action_request.comment:
        comment = ReviewComment(
            entity_type=entity_type,
            entity_id=entity_id,
            comment=action_request.comment,
            created_by=current_user.user_id
        )
        db.add(comment)
    
    db.commit()
    db.refresh(entity)
    
    return {
        "message": f"Ação {action_request.action} executada com sucesso",
        "new_status": new_status.value,
        "entity": entity
    }

@router.put("/{entity_type}/{entity_id}/status")
@handle_errors
@track_revisions
@logging_aspect
@notification_aspect
def update_review_status(
    entity_type: str,
    entity_id: int,
    status_update: ReviewStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza o status de revisão de uma entidade.
    """
    entity = _get_entity(db, entity_type, entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail=f"{entity_type} não encontrado")
    
    # Atualizar status
    old_status = entity.status
    entity.status = status_update.status.value
    entity.updated_at = datetime.utcnow()
    
    # Registrar mudança no histórico
    status_history = ReviewStatusHistory(
        entity_type=entity_type,
        entity_id=entity_id,
        old_status=old_status,
        new_status=status_update.status.value,
        changed_by=current_user.user_id,
        reason=status_update.reason
    )
    
    db.add(status_history)
    
    # Adicionar comentário se fornecido
    if status_update.comment:
        comment = ReviewComment(
            entity_type=entity_type,
            entity_id=entity_id,
            comment=status_update.comment,
            created_by=current_user.user_id
        )
        db.add(comment)
    
    db.commit()
    db.refresh(entity)
    
    return {
        "message": "Status atualizado com sucesso",
        "new_status": status_update.status.value,
        "entity": entity
    }

# --- INFORMAÇÕES DE REVISÃO ---

@router.get("/{entity_type}/{entity_id}/info", response_model=EntityReviewInfo)
@handle_errors
@logging_aspect
def get_review_info(
    entity_type: str,
    entity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém informações de revisão de uma entidade.
    """
    entity = _get_entity(db, entity_type, entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail=f"{entity_type} não encontrado")
    
    # Contar comentários
    total_comments = db.query(ReviewComment).filter(
        ReviewComment.entity_type == entity_type,
        ReviewComment.entity_id == entity_id
    ).count()
    
    # Contar comentários pendentes (sugestões)
    pending_reviews = db.query(ReviewComment).filter(
        ReviewComment.entity_type == entity_type,
        ReviewComment.entity_id == entity_id,
        ReviewComment.is_suggestion == True
    ).count()
    
    # Última revisão
    last_review = db.query(ReviewStatusHistory).filter(
        ReviewStatusHistory.entity_type == entity_type,
        ReviewStatusHistory.entity_id == entity_id
    ).order_by(ReviewStatusHistory.changed_at.desc()).first()
    
    return EntityReviewInfo(
        entity_type=entity_type,
        entity_id=entity_id,
        current_status=ReviewStatus(entity.status),
        total_comments=total_comments,
        pending_reviews=pending_reviews,
        last_review_date=last_review.changed_at if last_review else None,
        reviewed_by=last_review.user.name if last_review else None
    )

@router.get("/{entity_type}/{entity_id}/summary", response_model=ReviewSummary)
@handle_errors
@logging_aspect
def get_review_summary(
    entity_type: str,
    entity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém resumo completo das revisões de uma entidade.
    """
    entity = _get_entity(db, entity_type, entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail=f"{entity_type} não encontrado")
    
    # Informações da entidade
    entity_info = get_review_info(entity_type, entity_id, db, current_user)
    
    # Comentários
    comments = db.query(ReviewComment).filter(
        ReviewComment.entity_type == entity_type,
        ReviewComment.entity_id == entity_id
    ).order_by(ReviewComment.created_at.desc()).all()
    
    # Histórico de status
    status_history = db.query(ReviewStatusHistory).filter(
        ReviewStatusHistory.entity_type == entity_type,
        ReviewStatusHistory.entity_id == entity_id
    ).order_by(ReviewStatusHistory.changed_at.desc()).all()
    
    # Converter para dict para facilitar serialização
    status_history_dicts = []
    for history in status_history:
        status_history_dicts.append({
            "history_id": history.history_id,
            "old_status": history.old_status,
            "new_status": history.new_status,
            "changed_by": history.user.name if history.user else "Usuário",
            "reason": history.reason,
            "changed_at": history.changed_at
        })
    
    return ReviewSummary(
        entity_info=entity_info,
        comments=comments,
        status_history=status_history_dicts
    )

# --- FUNÇÕES AUXILIARES ---

def _get_entity(db: Session, entity_type: str, entity_id: int):
    """
    Obtém uma entidade do banco de dados baseado no tipo e ID.
    """
    entity_map = {
        "epic": Epic,
        "user_story": UserStory,
        "requirement": Requirement,
        "backlog": Backlog,
    }
    
    model_class = entity_map.get(entity_type)
    if not model_class:
        raise HTTPException(status_code=400, detail="Tipo de entidade inválido")
    
    return db.query(model_class).filter(
        getattr(model_class, f"{entity_type.split('_')[0]}_id") == entity_id
    ).first() 