import inspect
from typing import Callable, Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.base import BaseTrigger

from db.database import JOB_STORES
from utils.random import random_str

SCHEDULER = AsyncIOScheduler(jobstores=JOB_STORES)


def add_background_job(func: Callable[..., Any],
                       kwargs: dict[str, Any],
                       trigger: BaseTrigger,
                       override: bool = False) -> None:
    job_id = f"{inspect.getmodule(func).__name__}.{func.__name__}"
    job_id = job_id if override else f"{job_id}_{random_str(6)}"
    SCHEDULER.add_job(func=func, trigger=trigger, kwargs=kwargs, id=job_id, replace_existing=True)
