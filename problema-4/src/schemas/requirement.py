"""
Schemas Pydantic para a entidade Requirement (Requisito).
- RequirementCreate: dados necessários para criar um requisito.
- RequirementInDB: dados retornados do banco de dados para um requisito.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .review import ReviewStatus

class RequirementCreate(BaseModel):
    """Dados necessários para criar um requisito."""
    story_id: int = Field(..., description="ID da história de usuário ao qual pertence")
    description: str = Field(..., min_length=1, max_length=1000, description="Descrição do requisito")
    technical_details: Optional[str] = Field(None, max_length=2000, description="Detalhes técnicos")
    priority: Optional[int] = Field(3, ge=1, le=5, description="Prioridade de 1 a 5")
    status: Optional[ReviewStatus] = Field(ReviewStatus.DRAFT, description="Status de revisão do requisito")

class RequirementInDB(RequirementCreate):
    """Representação de um requisito armazenado no banco de dados."""
    requirement_id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True 