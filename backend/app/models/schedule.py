"""Search schedule database model."""
from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class SearchSchedule(Base):
    """Search schedule model for automated job searches."""

    __tablename__ = "search_schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    search_query: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=True)
    sources: Mapped[str] = mapped_column(String(500), default="all")  # Comma-separated sources
    cron_expression: Mapped[str] = mapped_column(String(100), nullable=False)  # Cron schedule
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_run: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    next_run: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user = relationship("User", back_populates="search_schedules")
