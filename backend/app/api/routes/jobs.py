"""Job routes."""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user
from app.db.database import get_db
from app.models.job import Job
from app.models.user import User
from app.schemas.job import JobCreate, JobResponse, JobSearchRequest, JobUpdate
from app.services.ranking import ranking_service
from app.services.scraper import scraper_service

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/search", response_model=List[JobResponse])
async def search_jobs(
    search_request: JobSearchRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Search for jobs and save them to the database."""
    # Scrape jobs from sources
    scraped_jobs = await scraper_service.scrape_jobs(
        query=search_request.query,
        location=search_request.location,
        sources=search_request.sources,
    )

    # Create job records
    jobs = []
    for job_data in scraped_jobs:
        job = Job(
            user_id=current_user.id,
            title=job_data.title,
            company=job_data.company,
            location=job_data.location,
            description=job_data.description,
            url=job_data.url,
            source=job_data.source,
            salary_min=job_data.salary_min,
            salary_max=job_data.salary_max,
        )
        jobs.append(job)

    # Rank jobs based on user profile
    ranked_jobs = ranking_service.rank_jobs(jobs, current_user)

    # Save to database
    for job in ranked_jobs:
        db.add(job)
    await db.commit()

    # Refresh all jobs to get IDs
    for job in ranked_jobs:
        await db.refresh(job)

    return ranked_jobs


@router.get("", response_model=List[JobResponse])
async def get_jobs(
    status: Optional[str] = Query(None, description="Filter by status"),
    min_score: Optional[float] = Query(None, description="Minimum match score"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all jobs for the current user."""
    query = select(Job).where(Job.user_id == current_user.id)

    if status:
        query = query.where(Job.status == status)
    if min_score is not None:
        query = query.where(Job.match_score >= min_score)

    query = query.order_by(Job.match_score.desc())

    result = await db.execute(query)
    jobs = result.scalars().all()

    return jobs


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific job."""
    result = await db.execute(
        select(Job).where(Job.id == job_id, Job.user_id == current_user.id)
    )
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    return job


@router.patch("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int,
    job_update: JobUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a job status."""
    result = await db.execute(
        select(Job).where(Job.id == job_id, Job.user_id == current_user.id)
    )
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    if job_update.status is not None:
        job.status = job_update.status

    await db.commit()
    await db.refresh(job)

    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a job."""
    result = await db.execute(
        select(Job).where(Job.id == job_id, Job.user_id == current_user.id)
    )
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    await db.delete(job)
    await db.commit()
