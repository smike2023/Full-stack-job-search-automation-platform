"""Application configuration settings."""
import secrets
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "Job Search Automation Platform"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./job_search.db"

    # OpenAI
    OPENAI_API_KEY: str = ""

    # Job scraping settings
    SCRAPE_INTERVAL_MINUTES: int = 60

    class Config:
        """Pydantic config."""

        env_file = ".env"
        extra = "ignore"


settings = Settings()
