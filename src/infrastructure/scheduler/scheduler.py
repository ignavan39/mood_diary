import logging
from typing import Callable, Coroutine, Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)


class AppScheduler:
    def __init__(self, timezone: str = "Europe/Moscow"):
        self.scheduler = AsyncIOScheduler(
            timezone=timezone,
            job_defaults={
                "coalesce": True,
                "max_instances": 2,
                "misfire_grace_time": 300,
            },
        )

    def add_cron_job(
        self,
        func: Callable[..., Coroutine[Any, Any, None]],
        *,
        id: str,
        name: str | None = None,
        hour: int | str = "*",
        minute: int | str = "*",
        day_of_week: str = "*",
        args: tuple | None = None,
        kwargs: dict | None = None,
    ) -> None:
        self.scheduler.add_job(
            func,
            trigger=CronTrigger(
                hour=hour,
                minute=minute,
                day_of_week=day_of_week,
            ),
            id=id,
            name=name or id,
            args=args or (),
            kwargs=kwargs or {},
        )
        logger.info("Registered cron job: %s (%s:%s)", id, hour, minute)

    def add_interval_job(
        self,
        func: Callable[..., Coroutine[Any, Any, None]],
        *,
        id: str,
        name: str | None = None,
        minutes: int = 1,
        args: tuple | None = None,
        kwargs: dict | None = None,
    ) -> None:
        self.scheduler.add_job(
            func,
            trigger=IntervalTrigger(minutes=minutes),
            id=id,
            name=name or id,
            args=args or (),
            kwargs=kwargs or {},
        )
        logger.info("Registered interval job: %s (every %d min)", id, minutes)

    async def start(self) -> None:
        self.scheduler.start()
        logger.info(
            "Scheduler started with %d jobs", len(self.scheduler.get_jobs())
        )

    async def shutdown(self) -> None:
        if self.scheduler.running:
            self.scheduler.shutdown(wait=True)
            logger.info("Scheduler stopped gracefully")