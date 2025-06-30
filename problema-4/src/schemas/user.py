from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Schema base para usuário, com email e nome."""
    email: EmailStr = Field(..., example="user@email.com")
    name: str = Field(..., min_length=2, max_length=100, example="João da Silva")

class UserCreate(UserBase):
    """Schema para criação de usuário (inclui senha)."""
    password: str = Field(..., min_length=6, example="senha123")

class UserLogin(BaseModel):
    """Schema para login de usuário."""
    email: EmailStr = Field(..., example="user@email.com")
    password: str = Field(..., min_length=6, example="senha123")

class UserInDB(UserBase):
    """Schema completo de usuário retornado pela API e usado internamente."""
    user_id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        orm_mode = True 