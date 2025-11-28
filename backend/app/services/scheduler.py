"""Scheduling service for automated job searches."""
from datetime import datetime
from typing import Dict, Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.models.schedule import SearchSchedule


class SchedulerService:
    """Service for managing scheduled job searches."""

    def __init__(self):
        """Initialize the scheduler service."""
        self.scheduler: Optional[AsyncIOScheduler] = None
        self.active_jobs: Dict[int, str] = {}  # schedule_id -> job_id mapping

    def start(self):
        """Start the scheduler."""
        if self.scheduler is None:
            self.scheduler = AsyncIOScheduler()
            self.scheduler.start()

    def stop(self):
        """Stop the scheduler."""
        if self.scheduler:
            self.scheduler.shutdown()
            self.scheduler = None
            self.active_jobs.clear()

    def add_job(
        self,
        schedule: SearchSchedule,
        job_func,
        *args,
        **kwargs,
    ) -> str:
        """Add a scheduled job.

        Args:
            schedule: SearchSchedule instance
            job_func: Function to execute
            *args: Arguments for the function
            **kwargs: Keyword arguments for the function

        Returns:
            Job ID
        """
        if self.scheduler is None:
            self.start()

        # Parse cron expression
        cron_parts = schedule.cron_expression.split()
        if len(cron_parts) != 5:
            raise ValueError("Invalid cron expression. Expected 5 parts: minute hour day month weekday")

        trigger = CronTrigger(
            minute=cron_parts[0],
            hour=cron_parts[1],
            day=cron_parts[2],
            month=cron_parts[3],
            day_of_week=cron_parts[4],
        )

        job = self.scheduler.add_job(
            job_func,
            trigger,
            args=args,
            kwargs=kwargs,
            id=f"search_{schedule.id}",
            replace_existing=True,
        )

        self.active_jobs[schedule.id] = job.id
        return job.id

    def remove_job(self, schedule_id: int) -> bool:
        """Remove a scheduled job.

        Args:
            schedule_id: ID of the schedule

        Returns:
            True if job was removed, False if not found
        """
        if schedule_id in self.active_jobs:
            job_id = self.active_jobs[schedule_id]
            if self.scheduler:
                try:
                    self.scheduler.remove_job(job_id)
                except Exception:
                    pass
            del self.active_jobs[schedule_id]
            return True
        return False

    def get_next_run_time(self, schedule_id: int) -> Optional[datetime]:
        """Get the next run time for a scheduled job.

        Args:
            schedule_id: ID of the schedule

        Returns:
            Next run time or None if not scheduled
        """
        if schedule_id in self.active_jobs and self.scheduler:
            job_id = self.active_jobs[schedule_id]
            job = self.scheduler.get_job(job_id)
            if job:
                return job.next_run_time
        return None


scheduler_service = SchedulerService()
