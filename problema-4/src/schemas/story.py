"""
Schemas Pydantic para a entidade UserStory (História de Usuário).
- UserStoryCreate: dados necessários para criar uma história de usuário.
- UserStoryInDB: dados retornados do banco de dados para uma história de usuário.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .review import ReviewStatus

class UserStoryCreate(BaseModel):
    """Dados necessários para criar uma história de usuário."""
    epic_id: int = Field(..., description="ID do épico ao qual pertence")
    persona_id: Optional[int] = Field(None, description="ID da persona associada")
    as_a: str = Field(..., min_length=1, max_length=500, description="Como [persona]")
    i_want: str = Field(..., min_length=1, max_length=500, description="Eu quero [objetivo]")
    so_that: str = Field(..., min_length=1, max_length=500, description="Para que [benefício]")
    acceptance_criteria: Optional[List[str]] = Field(None, description="Critérios de aceitação")
    priority: Optional[int] = Field(3, ge=1, le=5, description="Prioridade de 1 a 5")
    status: Optional[ReviewStatus] = Field(ReviewStatus.DRAFT, description="Status de revisão da história")
    generated_by_llm: Optional[bool] = Field(False, description="Se foi gerada por LLM")
    llm_prompt_used: Optional[str] = Field(None, description="Prompt usado na geração")

class UserStoryInDB(UserStoryCreate):
    """Representação de uma história de usuário armazenada no banco de dados."""
    story_id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True 