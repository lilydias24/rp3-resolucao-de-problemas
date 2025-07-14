"""
Schemas Pydantic para geração automática de backlog.
- BacklogGenerationRequest: parâmetros para geração automática
- BacklogGenerationResponse: resultado da geração
- BacklogGenerationOptions: opções de configuração
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class GenerationStrategy(str, Enum):
    """Estratégias de geração de backlog"""
    PRIORITY_BASED = "priority_based"      # Baseado em prioridade
    EPIC_BASED = "epic_based"              # Agrupado por épicos
    STORY_ONLY = "story_only"              # Apenas histórias de usuário
    REQUIREMENT_ONLY = "requirement_only"  # Apenas requisitos
    MIXED = "mixed"                        # Histórias e requisitos misturados

class BacklogGenerationRequest(BaseModel):
    """Dados para solicitar geração automática de backlog"""
    product_id: int = Field(..., description="ID do produto")
    name: str = Field(..., min_length=1, max_length=255, description="Nome do backlog")
    description: Optional[str] = Field(None, description="Descrição do backlog")
    version: Optional[str] = Field(None, description="Versão do backlog")
    strategy: GenerationStrategy = Field(
        GenerationStrategy.PRIORITY_BASED, 
        description="Estratégia de geração"
    )
    include_stories: bool = Field(True, description="Incluir histórias de usuário aprovadas")
    include_requirements: bool = Field(True, description="Incluir requisitos aprovados")
    min_priority: Optional[int] = Field(3, ge=1, le=5, description="Prioridade mínima para inclusão")
    max_items: Optional[int] = Field(None, ge=1, le=1000, description="Número máximo de itens")
    group_by_epic: bool = Field(False, description="Agrupar itens por épico")
    auto_prioritize: bool = Field(True, description="Priorizar automaticamente baseado em critérios")

class BacklogGenerationOptions(BaseModel):
    """Opções avançadas para geração de backlog"""
    story_weight: float = Field(1.0, ge=0.1, le=10.0, description="Peso das histórias de usuário")
    requirement_weight: float = Field(0.8, ge=0.1, le=10.0, description="Peso dos requisitos")
    priority_multiplier: float = Field(1.5, ge=1.0, le=5.0, description="Multiplicador de prioridade")
    recent_bonus: float = Field(0.2, ge=0.0, le=1.0, description="Bônus para itens recentes")
    complexity_factor: bool = Field(True, description="Considerar complexidade na priorização")

class BacklogItemInfo(BaseModel):
    """Informações de um item do backlog gerado"""
    item_id: int
    item_type: str  # 'story' ou 'requirement'
    title: str
    description: str
    priority: int
    epic_title: Optional[str] = None
    estimated_effort: Optional[str] = None
    business_value: Optional[int] = None
    position: int

class BacklogGenerationResponse(BaseModel):
    """Resposta da geração automática de backlog"""
    backlog_id: int
    backlog_name: str
    total_items: int
    stories_count: int
    requirements_count: int
    generation_strategy: GenerationStrategy
    generation_options: BacklogGenerationOptions
    items: List[BacklogItemInfo]
    summary: Dict[str, Any]
    created_at: datetime

class BacklogGenerationPreview(BaseModel):
    """Preview da geração antes de confirmar"""
    estimated_items: int
    estimated_stories: int
    estimated_requirements: int
    preview_items: List[BacklogItemInfo]
    strategy: GenerationStrategy
    options: BacklogGenerationOptions 