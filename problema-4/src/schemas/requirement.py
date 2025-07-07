"""
Schemas Pydantic para a entidade Requirement (Requisito).
- RequirementCreate: dados necessários para criar um requisito.
- RequirementInDB: dados retornados do banco de dados para um requisito.
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RequirementCreate(BaseModel):
    """Dados necessários para criar um requisito."""
    story_id: int
    description: str
    technical_details: Optional[str] = None
    priority: Optional[int] = 3
    status: Optional[str] = 'draft'

class RequirementInDB(RequirementCreate):
    """Representação de um requisito armazenado no banco de dados."""
    requirement_id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True 