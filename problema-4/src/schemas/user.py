from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Schema base para usuário, com email e nome."""
    email: EmailStr
    name: str

class UserCreate(BaseModel):
    """Schema para criação de usuário (inclui senha)."""
    password: str
    email: EmailStr
    name: str
    # role: str = "user"  # Valor padrão

class UserLogin(BaseModel):
    """Schema para login de usuário."""
    email: EmailStr
    password: str

class UserInDB(UserBase):
    """Schema completo de usuário retornado pela API e usado internamente."""
    user_id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True 