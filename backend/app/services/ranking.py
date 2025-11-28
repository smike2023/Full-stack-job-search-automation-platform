"""Job ranking service."""
import re
from typing import List, Tuple

from app.models.job import Job
from app.models.user import User


class JobRankingService:
    """Service for ranking jobs based on user skills and keywords."""

    def calculate_match_score(
        self, job: Job, user_skills: List[str], user_keywords: List[str]
    ) -> Tuple[float, List[str], List[str]]:
        """Calculate match score between job and user profile.

        Args:
            job: Job instance to score
            user_skills: List of user's skills
            user_keywords: List of user's preferred keywords

        Returns:
            Tuple of (score, matched_skills, matched_keywords)
        """
        job_text = f"{job.title} {job.description or ''}".lower()
        
        matched_skills = []
        matched_keywords = []
        
        # Match skills (weighted higher)
        for skill in user_skills:
            skill_lower = skill.lower().strip()
            if skill_lower and skill_lower in job_text:
                matched_skills.append(skill)
        
        # Match keywords
        for keyword in user_keywords:
            keyword_lower = keyword.lower().strip()
            if keyword_lower and keyword_lower in job_text:
                matched_keywords.append(keyword)
        
        # Calculate score (skills are weighted 2x)
        total_possible = len(user_skills) * 2 + len(user_keywords)
        if total_possible == 0:
            return 0.0, [], []
        
        score = (len(matched_skills) * 2 + len(matched_keywords)) / total_possible * 100
        
        return round(score, 2), matched_skills, matched_keywords

    def rank_jobs(
        self, jobs: List[Job], user: User
    ) -> List[Job]:
        """Rank a list of jobs based on user profile.

        Args:
            jobs: List of jobs to rank
            user: User instance with skills and keywords

        Returns:
            List of jobs sorted by match score (descending)
        """
        user_skills = []
        user_keywords = []
        
        if user.skills:
            user_skills = [s.strip() for s in user.skills.split(",") if s.strip()]
        if user.keywords:
            user_keywords = [k.strip() for k in user.keywords.split(",") if k.strip()]
        
        for job in jobs:
            score, matched_skills, matched_keywords = self.calculate_match_score(
                job, user_skills, user_keywords
            )
            job.match_score = score
            job.matched_skills = ",".join(matched_skills) if matched_skills else None
            job.matched_keywords = ",".join(matched_keywords) if matched_keywords else None
        
        return sorted(jobs, key=lambda x: x.match_score, reverse=True)


ranking_service = JobRankingService()
