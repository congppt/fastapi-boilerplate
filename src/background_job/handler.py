import inspect
from typing import Callable, Any

from apscheduler.triggers.base import BaseTrigger

from background_job import SCHEDULER
from utils.random import random_str



def add_background_job(func: Callable[..., Any],
                       kwargs: dict[str, Any],
                       trigger: BaseTrigger,
                       override: bool = False) -> None:
    """
    Schedule a background job
    :param func: reference to job function
    :param kwargs: keyword arguments to pass to the job function
    :param trigger: job trigger
    :param override: override the existing job
    """
    job_id = f"{inspect.getmodule(func).__name__}.{func.__name__}"
    job_id = job_id if override else f"{job_id}_{random_str(6)}"
    SCHEDULER.add_job(func=func, trigger=trigger, kwargs=kwargs, id=job_id, replace_existing=True)
