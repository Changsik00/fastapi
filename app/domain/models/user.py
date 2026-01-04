from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import EmailStr

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True)
    is_active: bool = True
    role: UserRole = Field(default=UserRole.USER)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

# DTOs (Data Transfer Objects)
class Token(SQLModel):
    access_token: str
    token_type: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
