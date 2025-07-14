"""
Schemas Pydantic para a entidade Epic (Épico).
- EpicCreate: dados necessários para criar um épico.
- EpicInDB: dados retornados do banco de dados para um épico.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .review import ReviewStatus

class EpicCreate(BaseModel):
    """Dados necessários para criar um épico."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[ReviewStatus] = Field(ReviewStatus.DRAFT, description="Status de revisão do épico")

class EpicInDB(EpicCreate):
    """Representação de um épico armazenado no banco de dados."""
    epic_id: int
    product_id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True 