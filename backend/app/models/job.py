"""Job database model."""
from datetime import datetime, timezone
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Job(Base):
    """Job model for storing scraped job listings."""

    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    url: Mapped[str] = mapped_column(String(1000), nullable=False)
    source: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g., "linkedin", "indeed"
    salary_min: Mapped[float] = mapped_column(Float, nullable=True)
    salary_max: Mapped[float] = mapped_column(Float, nullable=True)
    match_score: Mapped[float] = mapped_column(Float, default=0.0)  # Ranking score
    matched_skills: Mapped[str] = mapped_column(String(1000), nullable=True)  # Comma-separated matched skills
    matched_keywords: Mapped[str] = mapped_column(String(1000), nullable=True)  # Comma-separated matched keywords
    status: Mapped[str] = mapped_column(String(50), default="new")  # new, applied, rejected, interview
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    user = relationship("User", back_populates="jobs")
