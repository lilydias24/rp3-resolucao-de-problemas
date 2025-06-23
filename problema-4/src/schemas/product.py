from typing import List, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime

class ProductBase(BaseModel):
    """Base schema com campos comuns"""
    name: str = Field(..., min_length=3, max_length=255, example="Meu Produto")
    description: Optional[str] = Field(
        None,
        max_length=2000,
        example="Um sistema para gerenciar histórias de usuário"
    )
    value_proposition: Optional[str] = Field(
        None,
        alias="valueProposition",
        max_length=1000,
        example="Automatizar a criação de user stories com IA"
    )
    platforms: Optional[List[str]] = Field(
        ["web"],
        example=["web", "mobile"]
    )

class ProductCreate(ProductBase):
    """Schema para criação de produto (pode adicionar campos específicos)"""
    
    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('O nome deve conter espaços')
        return v.title()
    
    @validator('platforms')
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
    """Schema completo retornado pela API"""
    product_id: int = Field(..., example=42)
    created_by: int = Field(..., example=123)
    created_at: datetime = Field(..., example="2023-11-21T10:00:00Z")
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True  # Permite conversão de ORM para schema
        allow_population_by_field_name = True  # Permite usar alias