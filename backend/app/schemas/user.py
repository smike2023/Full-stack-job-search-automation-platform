"""User schemas for request/response validation."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user."""

    password: str
    skills: Optional[str] = None
    keywords: Optional[str] = None


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    full_name: Optional[str] = None
    skills: Optional[str] = None
    keywords: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response."""

    id: int
    skills: Optional[str] = None
    keywords: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class Token(BaseModel):
    """Schema for authentication token."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token data."""

    email: Optional[str] = None


class LoginRequest(BaseModel):
    """Schema for login request."""

    email: EmailStr
    password: str
