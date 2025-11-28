"""Resume schemas for request/response validation."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ResumeBase(BaseModel):
    """Base resume schema."""

    title: str
    target_role: Optional[str] = None
    target_company: Optional[str] = None


class ResumeCreate(ResumeBase):
    """Schema for creating a resume."""

    job_id: Optional[int] = None
    user_profile: Optional[str] = None  # User's base resume/profile
    job_description: Optional[str] = None  # Target job description for tailoring


class ResumeUpdate(BaseModel):
    """Schema for updating a resume."""

    title: Optional[str] = None
    content: Optional[str] = None
    target_role: Optional[str] = None
    target_company: Optional[str] = None


class ResumeResponse(ResumeBase):
    """Schema for resume response."""

    id: int
    user_id: int
    job_id: Optional[int] = None
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class ResumeGenerateRequest(BaseModel):
    """Schema for AI resume generation request."""

    job_id: Optional[int] = None
    target_role: str
    target_company: Optional[str] = None
    job_description: Optional[str] = None
    user_experience: str
    user_skills: str
    user_education: Optional[str] = None
