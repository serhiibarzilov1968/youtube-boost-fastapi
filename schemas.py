# schemas.py - Полная версия

from pydantic import BaseModel, EmailStr
from typing import List, Optional

# --- Схемы для Пользователей (Users) ---

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True # Позволяет Pydantic работать с объектами SQLAlchemy

# --- Схемы для Аутентификации (Auth) ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class TokenRequest(BaseModel):
    email: str
    password: str

# --- Схемы для Услуг (Services) ---

class SeoRequest(BaseModel):
    topic: str

class DesignRequest(BaseModel):
    prompt: str
    style: str

class ShortsRequest(BaseModel):
    video_id: str
