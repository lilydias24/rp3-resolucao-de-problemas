"""
Schemas Pydantic para a entidade UserStory (História de Usuário).
- UserStoryCreate: dados necessários para criar uma história de usuário.
- UserStoryInDB: dados retornados do banco de dados para uma história de usuário.
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserStoryCreate(BaseModel):
    """Dados necessários para criar uma história de usuário."""
    epic_id: int
    persona_id: Optional[int] = None
    as_a: str
    i_want: str
    so_that: str
    acceptance_criteria: Optional[List[str]] = None
    priority: Optional[int] = 3
    status: Optional[str] = 'draft'
    generated_by_llm: Optional[bool] = False
    llm_prompt_used: Optional[str] = None

class UserStoryInDB(UserStoryCreate):
    """Representação de uma história de usuário armazenada no banco de dados."""
    story_id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True 