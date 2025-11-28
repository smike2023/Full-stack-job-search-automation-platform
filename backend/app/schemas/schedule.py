"""Schedule schemas for request/response validation."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ScheduleBase(BaseModel):
    """Base schedule schema."""

    name: str
    search_query: str
    location: Optional[str] = None
    sources: str = "all"
    cron_expression: str


class ScheduleCreate(ScheduleBase):
    """Schema for creating a schedule."""

    pass


class ScheduleUpdate(BaseModel):
    """Schema for updating a schedule."""

    name: Optional[str] = None
    search_query: Optional[str] = None
    location: Optional[str] = None
    sources: Optional[str] = None
    cron_expression: Optional[str] = None
    is_active: Optional[bool] = None


class ScheduleResponse(ScheduleBase):
    """Schema for schedule response."""

    id: int
    user_id: int
    is_active: bool
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True
