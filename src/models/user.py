from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import EmailStr, field_validator

class UserBase(SQLModel):
    username: str = Field(min_length=3, max_length=50, unique=True)
    email: EmailStr = Field(unique=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str

class UserCreate(UserBase):
    password: str = Field(min_length=8)
    password_confirm: str
    
    @field_validator('password_confirm')
    @classmethod
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v

class UserUpdate(SQLModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    password_confirm: Optional[str] = None
    
    @field_validator('password_confirm')
    @classmethod
    def passwords_match(cls, v, info):
        if v is not None and 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v

class UserResponse(UserBase):
    id: int