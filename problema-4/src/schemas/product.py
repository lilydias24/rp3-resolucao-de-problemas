"""
Schemas Pydantic para a entidade Product (Produto).
- ProductCreate: dados necessários para criar um produto.
- ProductInDB: dados retornados do banco de dados para um produto.
"""
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime

class ProductBase(BaseModel):
    """Base schema com campos comuns"""
    name: str = Field(..., min_length=3, max_length=255, json_schema_extra={"example": "Meu Produto"})
    description: Optional[str] = Field(
        None,
        max_length=2000,
        json_schema_extra={"example": "Um sistema para gerenciar histórias de usuário"}
    )
    value_proposition: Optional[str] = Field(
        None,
        alias="valueProposition",
        max_length=1000,
        json_schema_extra={"example": "Automatizar a criação de user stories com IA"}
    )
    platforms: Optional[List[str]] = Field(
        ["web"],
        json_schema_extra={"example": ["web", "mobile"]}
    )

class ProductCreate(ProductBase):
    """Dados necessários para criar um produto."""
    @field_validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('O nome deve conter espaços')
        return v.title()
    
    @field_validator('platforms')
    def validate_platforms(cls, v):
        valid_platforms = ["web", "mobile", "desktop", "api"]
        for platform in v:
            if platform not in valid_platforms:
                raise ValueError(f"Plataforma inválida: {platform}. Use: {valid_platforms}")
        return v

class ProductUpdate(BaseModel):
    """Schema para atualização de produto (campos opcionais)"""
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str]
    value_proposition: Optional[str]
    platforms: Optional[List[str]]

class ProductInDB(ProductBase):
    """Representação de um produto armazenado no banco de dados."""
    product_id: int = Field(..., json_schema_extra={"example": 42})
    created_by: int = Field(..., json_schema_extra={"example": 123})
    created_at: datetime = Field(..., json_schema_extra={"example": "2023-11-21T10:00:00Z"})
    updated_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True, validate_by_name=True)