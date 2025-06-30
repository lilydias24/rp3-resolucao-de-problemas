from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr = Field(..., example="user@email.com")
    name: str = Field(..., min_length=2, max_length=100, example="João da Silva")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, example="senha123")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="user@email.com")
    password: str = Field(..., min_length=6, example="senha123")

class UserInDB(UserBase):
    user_id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        orm_mode = True 