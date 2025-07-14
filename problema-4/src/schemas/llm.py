from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class LLMRequest(BaseModel):
    """Schema para requisições de geração LLM"""
    product_id: int = Field(..., description="ID do produto para o qual as histórias serão geradas")
    epic_ids: Optional[List[int]] = Field(None, description="Lista de IDs de épicos para os quais gerar histórias")
    productInfo: str = Field(..., description="Informações do produto para geração")
    userPromptAdjustment: Optional[str] = Field(None, description="Ajuste personalizado do prompt")
    epicsSummary: Optional[str] = Field(None, description="Resumo dos épicos (para geração de histórias)")
    userStories: Optional[str] = Field(None, description="Histórias de usuário (para geração de requisitos)")

class LLMResponse(BaseModel):
    """Schema para respostas de geração LLM"""
    content: List[Dict[str, Any]] = Field(..., description="Lista de épicos gerados pela LLM (título e descrição)")
    success: bool = Field(True, description="Indica se a geração foi bem-sucedida")
    message: Optional[str] = Field(None, description="Mensagem adicional")