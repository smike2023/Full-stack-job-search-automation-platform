"""Job scraping service."""
from typing import List, Optional

from app.schemas.job import JobCreate


class JobScraperService:
    """Service for scraping jobs from various job boards."""

    def __init__(self):
        """Initialize the scraper service."""
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    async def scrape_jobs(
        self,
        query: str,
        location: Optional[str] = None,
        sources: List[str] = None,
    ) -> List[JobCreate]:
        """Scrape jobs from multiple sources."""
        if sources is None:
            sources = ["mock"]

        all_jobs = []

        for source in sources:
            if source == "mock" or source == "all":
                jobs = await self._scrape_mock_jobs(query, location)
                all_jobs.extend(jobs)

        return all_jobs

    async def _scrape_mock_jobs(
        self, query: str, location: Optional[str] = None
    ) -> List[JobCreate]:
        """Generate mock job data for demonstration."""
        # In production, this would scrape real job boards
        mock_jobs = [
            JobCreate(
                title=f"Senior {query} Developer",
                company="Tech Corp",
                location=location or "Remote",
                description=f"We are looking for a Senior {query} Developer with 5+ years of experience.",
                url="https://example.com/job/1",
                source="mock",
                salary_min=80000,
                salary_max=120000,
            ),
            JobCreate(
                title=f"{query} Engineer",
                company="Startup Inc",
                location=location or "New York, NY",
                description=f"Join our team as a {query} Engineer. Experience with modern frameworks required.",
                url="https://example.com/job/2",
                source="mock",
                salary_min=70000,
                salary_max=100000,
            ),
            JobCreate(
                title=f"Lead {query} Architect",
                company="Enterprise Solutions",
                location=location or "San Francisco, CA",
                description=f"Lead our {query} architecture team. 8+ years experience required.",
                url="https://example.com/job/3",
                source="mock",
                salary_min=150000,
                salary_max=200000,
            ),
            JobCreate(
                title=f"Junior {query} Developer",
                company="Growth Company",
                location=location or "Austin, TX",
                description=f"Entry-level position for {query} enthusiasts. Training provided.",
                url="https://example.com/job/4",
                source="mock",
                salary_min=50000,
                salary_max=70000,
            ),
            JobCreate(
                title=f"{query} Full Stack Developer",
                company="Innovation Labs",
                location=location or "Remote",
                description=f"Full stack development with focus on {query}. Cloud experience a plus.",
                url="https://example.com/job/5",
                source="mock",
                salary_min=90000,
                salary_max=140000,
            ),
        ]
        return mock_jobs


scraper_service = JobScraperService()
