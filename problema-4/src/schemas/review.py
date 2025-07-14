"""
Schemas Pydantic para o sistema de revisão/sugestão.
- ReviewComment: comentários/sugestões em entidades
- ReviewStatus: status de revisão das entidades
- ReviewAction: ações de aprovação/rejeição
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ReviewStatus(str, Enum):
    """Status possíveis para revisão de entidades"""
    DRAFT = "draft"                    # Rascunho inicial
    IN_REVIEW = "in_review"            # Em revisão
    APPROVED = "approved"              # Aprovado
    REJECTED = "rejected"              # Rejeitado
    NEEDS_REVISION = "needs_revision"  # Precisa de revisão
    IMPLEMENTED = "implemented"        # Implementado

class ReviewAction(str, Enum):
    """Ações possíveis de revisão"""
    SUBMIT_FOR_REVIEW = "submit_for_review"
    APPROVE = "approve"
    REJECT = "reject"
    REQUEST_REVISION = "request_revision"
    MARK_IMPLEMENTED = "mark_implemented"

class ReviewCommentCreate(BaseModel):
    """Dados necessários para criar um comentário de revisão"""
    entity_type: str = Field(..., description="Tipo da entidade (epic, user_story, requirement)")
    entity_id: int = Field(..., description="ID da entidade")
    comment: str = Field(..., min_length=1, max_length=2000, description="Comentário ou sugestão")
    is_suggestion: bool = Field(False, description="Se é uma sugestão de melhoria")
    suggested_changes: Optional[str] = Field(None, description="Sugestões específicas de mudanças")

class ReviewCommentInDB(ReviewCommentCreate):
    """Representação de um comentário de revisão armazenado no banco"""
    comment_id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ReviewActionRequest(BaseModel):
    """Dados para solicitar uma ação de revisão"""
    action: ReviewAction = Field(..., description="Ação a ser executada")
    comment: Optional[str] = Field(None, description="Comentário opcional sobre a ação")
    reason: Optional[str] = Field(None, description="Motivo da ação")

class ReviewStatusUpdate(BaseModel):
    """Dados para atualizar o status de revisão"""
    status: ReviewStatus = Field(..., description="Novo status")
    comment: Optional[str] = Field(None, description="Comentário sobre a mudança de status")
    reason: Optional[str] = Field(None, description="Motivo da mudança")

class EntityReviewInfo(BaseModel):
    """Informações de revisão de uma entidade"""
    entity_type: str
    entity_id: int
    current_status: ReviewStatus
    total_comments: int
    pending_reviews: int
    last_review_date: Optional[datetime] = None
    reviewed_by: Optional[str] = None

class ReviewSummary(BaseModel):
    """Resumo das revisões de uma entidade"""
    entity_info: EntityReviewInfo
    comments: List[ReviewCommentInDB]
    status_history: List[dict]  # Histórico de mudanças de status 