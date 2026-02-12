from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserOut(UserBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None


# Item schemas
class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class ItemOut(ItemBase):
    id: int
    owner_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
