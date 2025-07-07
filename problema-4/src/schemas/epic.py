"""
Schemas Pydantic para a entidade Epic (Épico).
- EpicCreate: dados necessários para criar um épico.
- EpicInDB: dados retornados do banco de dados para um épico.
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EpicCreate(BaseModel):
    """Dados necessários para criar um épico."""
    title: str
    description: Optional[str] = None
    status: Optional[str] = 'draft'

class EpicInDB(EpicCreate):
    """Representação de um épico armazenado no banco de dados."""
    epic_id: int
    product_id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True 