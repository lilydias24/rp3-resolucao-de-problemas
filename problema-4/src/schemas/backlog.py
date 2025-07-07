"""
Schemas Pydantic para as entidades Backlog e BacklogItem.
- BacklogCreate: dados necessários para criar um backlog.
- BacklogInDB: dados retornados do banco de dados para um backlog.
- BacklogItemCreate: dados necessários para criar um item do backlog.
- BacklogItemInDB: dados retornados do banco de dados para um item do backlog.
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class BacklogCreate(BaseModel):
    """Dados necessários para criar um backlog."""
    product_id: int
    name: str
    description: Optional[str] = None
    version: Optional[str] = None

class BacklogInDB(BacklogCreate):
    """Representação de um backlog armazenado no banco de dados."""
    backlog_id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class BacklogItemCreate(BaseModel):
    """Dados necessários para criar um item do backlog."""
    backlog_id: int
    story_id: Optional[int] = None
    requirement_id: Optional[int] = None
    position: int
    sprint_planned: Optional[str] = None

class BacklogItemInDB(BacklogItemCreate):
    """Representação de um item do backlog armazenado no banco de dados."""
    item_id: int

    class Config:
        orm_mode = True 