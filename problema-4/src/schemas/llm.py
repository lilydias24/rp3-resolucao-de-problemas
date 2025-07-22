from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class GenerateEpicsRequest(BaseModel):
    product_id: int = Field(..., description="ID do produto para gerar épicos")
    userPromptAdjustment: Optional[str] = Field(None, description="Ajuste personalizado do prompt")

class GenerateUserStoriesRequest(BaseModel):
    product_id: int = Field(..., description="ID do produto para gerar histórias")
    userPromptAdjustment: Optional[str] = Field(None, description="Ajuste personalizado do prompt")

class GenerateRequirementsRequest(BaseModel):
    story_id: int = Field(..., description="ID da história de usuário para gerar requisitos")
    userPromptAdjustment: Optional[str] = Field(None, description="Ajuste personalizado do prompt")

class LLMRequest(BaseModel):
    """Schema genérico para requisições LLM, pode ser usado se um endpoint precisar de mais flexibilidade"""
    product_id: Optional[int] = None
    epic_ids: Optional[List[int]] = None
    story_id: Optional[int] = None
    prompt: str
    custom_prompt: Optional[str] = None

class LLMResponse(BaseModel):
    """Schema para respostas de geração LLM"""
    content: List[Dict[str, Any]] = Field(..., description="Conteúdo gerado pela LLM")
    success: bool = Field(True, description="Indica se a geração foi bem-sucedida")
    message: Optional[str] = Field(None, description="Mensagem adicional")