"""Schedule routes."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user
from app.db.database import get_db
from app.models.schedule import SearchSchedule
from app.models.user import User
from app.schemas.schedule import ScheduleCreate, ScheduleResponse, ScheduleUpdate
from app.services.scheduler import scheduler_service

router = APIRouter(prefix="/schedules", tags=["schedules"])


@router.post("", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    schedule_in: ScheduleCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new search schedule."""
    schedule = SearchSchedule(
        user_id=current_user.id,
        name=schedule_in.name,
        search_query=schedule_in.search_query,
        location=schedule_in.location,
        sources=schedule_in.sources,
        cron_expression=schedule_in.cron_expression,
    )

    db.add(schedule)
    await db.commit()
    await db.refresh(schedule)

    # Calculate next run time
    next_run = scheduler_service.get_next_run_time(schedule.id)
    if next_run:
        schedule.next_run = next_run
        await db.commit()
        await db.refresh(schedule)

    return schedule


@router.get("", response_model=List[ScheduleResponse])
async def get_schedules(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all schedules for the current user."""
    result = await db.execute(
        select(SearchSchedule)
        .where(SearchSchedule.user_id == current_user.id)
        .order_by(SearchSchedule.created_at.desc())
    )
    schedules = result.scalars().all()

    return schedules


@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(
    schedule_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific schedule."""
    result = await db.execute(
        select(SearchSchedule).where(
            SearchSchedule.id == schedule_id, SearchSchedule.user_id == current_user.id
        )
    )
    schedule = result.scalar_one_or_none()

    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found",
        )

    return schedule


@router.put("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(
    schedule_id: int,
    schedule_update: ScheduleUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a schedule."""
    result = await db.execute(
        select(SearchSchedule).where(
            SearchSchedule.id == schedule_id, SearchSchedule.user_id == current_user.id
        )
    )
    schedule = result.scalar_one_or_none()

    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found",
        )

    if schedule_update.name is not None:
        schedule.name = schedule_update.name
    if schedule_update.search_query is not None:
        schedule.search_query = schedule_update.search_query
    if schedule_update.location is not None:
        schedule.location = schedule_update.location
    if schedule_update.sources is not None:
        schedule.sources = schedule_update.sources
    if schedule_update.cron_expression is not None:
        schedule.cron_expression = schedule_update.cron_expression
    if schedule_update.is_active is not None:
        schedule.is_active = schedule_update.is_active

    await db.commit()
    await db.refresh(schedule)

    return schedule


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(
    schedule_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a schedule."""
    result = await db.execute(
        select(SearchSchedule).where(
            SearchSchedule.id == schedule_id, SearchSchedule.user_id == current_user.id
        )
    )
    schedule = result.scalar_one_or_none()

    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found",
        )

    # Remove from scheduler
    scheduler_service.remove_job(schedule.id)

    await db.delete(schedule)
    await db.commit()


@router.post("/{schedule_id}/activate", response_model=ScheduleResponse)
async def activate_schedule(
    schedule_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Activate a schedule."""
    result = await db.execute(
        select(SearchSchedule).where(
            SearchSchedule.id == schedule_id, SearchSchedule.user_id == current_user.id
        )
    )
    schedule = result.scalar_one_or_none()

    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found",
        )

    schedule.is_active = True
    await db.commit()
    await db.refresh(schedule)

    return schedule


@router.post("/{schedule_id}/deactivate", response_model=ScheduleResponse)
async def deactivate_schedule(
    schedule_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Deactivate a schedule."""
    result = await db.execute(
        select(SearchSchedule).where(
            SearchSchedule.id == schedule_id, SearchSchedule.user_id == current_user.id
        )
    )
    schedule = result.scalar_one_or_none()

    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found",
        )

    schedule.is_active = False
    scheduler_service.remove_job(schedule.id)

    await db.commit()
    await db.refresh(schedule)

    return schedule
