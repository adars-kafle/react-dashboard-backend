from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        from_attributes = True


class User(UserBase):
    id: UUID
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    message: str
    user: User


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserLogoutResponse(BaseModel):
    message: str


class TokenPayload(BaseModel):
    sub: str | None = None
