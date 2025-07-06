from pydantic import BaseModel, Field
from typing import Optional

class LLMRequest(BaseModel):
    """Schema para requisições de geração LLM"""
    productInfo: str = Field(..., description="Informações do produto para geração")
    userPromptAdjustment: Optional[str] = Field(None, description="Ajuste personalizado do prompt")
    epicsSummary: Optional[str] = Field(None, description="Resumo dos épicos (para geração de histórias)")
    userStories: Optional[str] = Field(None, description="Histórias de usuário (para geração de requisitos)")

class LLMResponse(BaseModel):
    """Schema para respostas de geração LLM"""
    content: str = Field(..., description="Conteúdo gerado pela LLM")
    success: bool = Field(True, description="Indica se a geração foi bem-sucedida")
    message: Optional[str] = Field(None, description="Mensagem adicional")