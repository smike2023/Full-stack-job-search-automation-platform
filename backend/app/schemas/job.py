"""Job schemas for request/response validation."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class JobBase(BaseModel):
    """Base job schema."""

    title: str
    company: str
    location: Optional[str] = None
    description: Optional[str] = None
    url: str
    source: str


class JobCreate(JobBase):
    """Schema for creating a job."""

    salary_min: Optional[float] = None
    salary_max: Optional[float] = None


class JobUpdate(BaseModel):
    """Schema for updating a job."""

    status: Optional[str] = None


class JobResponse(JobBase):
    """Schema for job response."""

    id: int
    user_id: int
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    match_score: float
    matched_skills: Optional[str] = None
    matched_keywords: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class JobSearchRequest(BaseModel):
    """Schema for job search request."""

    query: str
    location: Optional[str] = None
    sources: List[str] = ["all"]


class JobRankingResponse(BaseModel):
    """Schema for job ranking response."""

    jobs: List[JobResponse]
    total: int
