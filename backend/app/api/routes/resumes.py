"""Resume routes."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user
from app.db.database import get_db
from app.models.job import Job
from app.models.resume import Resume
from app.models.user import User
from app.schemas.resume import (
    ResumeCreate,
    ResumeGenerateRequest,
    ResumeResponse,
    ResumeUpdate,
)
from app.services.resume_generator import resume_generator_service

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("/generate", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def generate_resume(
    request: ResumeGenerateRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate a tailored resume using AI."""
    # Get job details if job_id is provided
    job_description = request.job_description
    target_company = request.target_company

    if request.job_id:
        result = await db.execute(
            select(Job).where(Job.id == request.job_id, Job.user_id == current_user.id)
        )
        job = result.scalar_one_or_none()
        if job:
            job_description = job_description or job.description
            target_company = target_company or job.company

    # Generate resume content
    content = await resume_generator_service.generate_resume(
        target_role=request.target_role,
        user_experience=request.user_experience,
        user_skills=request.user_skills,
        target_company=target_company,
        job_description=job_description,
        user_education=request.user_education,
    )

    # Save resume to database
    resume = Resume(
        user_id=current_user.id,
        job_id=request.job_id,
        title=f"Resume for {request.target_role}",
        content=content,
        target_role=request.target_role,
        target_company=target_company,
    )

    db.add(resume)
    await db.commit()
    await db.refresh(resume)

    return resume


@router.get("", response_model=List[ResumeResponse])
async def get_resumes(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all resumes for the current user."""
    result = await db.execute(
        select(Resume)
        .where(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
    )
    resumes = result.scalars().all()

    return resumes


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific resume."""
    result = await db.execute(
        select(Resume).where(Resume.id == resume_id, Resume.user_id == current_user.id)
    )
    resume = result.scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    return resume


@router.put("/{resume_id}", response_model=ResumeResponse)
async def update_resume(
    resume_id: int,
    resume_update: ResumeUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a resume."""
    result = await db.execute(
        select(Resume).where(Resume.id == resume_id, Resume.user_id == current_user.id)
    )
    resume = result.scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    if resume_update.title is not None:
        resume.title = resume_update.title
    if resume_update.content is not None:
        resume.content = resume_update.content
    if resume_update.target_role is not None:
        resume.target_role = resume_update.target_role
    if resume_update.target_company is not None:
        resume.target_company = resume_update.target_company

    await db.commit()
    await db.refresh(resume)

    return resume


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a resume."""
    result = await db.execute(
        select(Resume).where(Resume.id == resume_id, Resume.user_id == current_user.id)
    )
    resume = result.scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    await db.delete(resume)
    await db.commit()
