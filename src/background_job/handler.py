import inspect
import logging
from typing import Callable, Any

from apscheduler.events import JobExecutionEvent
from apscheduler.triggers.base import BaseTrigger

import logger
from background_job import SCHEDULER
from constants import MAX_JOB_RETRY
from utils.random import random_str



def add_background_job(func: Callable[..., Any],
                       kwargs: dict[str, Any],
                       trigger: BaseTrigger,
                       override: bool = False) -> None:
    """
    Schedule a background job
    :param func: reference to job function
    :param kwargs: keyword arguments passed into job function
    :param trigger: job trigger
    :param override: override the existing job
    """
    job_id = f"{inspect.getmodule(func).__name__}.{func.__name__}"
    job_id = job_id if override else f"{job_id}_{random_str(6)}"
    return SCHEDULER.add_job(func=func, trigger=trigger, kwargs=kwargs, id=job_id, replace_existing=True)

def listen_job_execute_error(event: JobExecutionEvent):
    job = SCHEDULER.get_job(event.job_id)
    max_retry = job.kwargs.get("max_retry", None) or MAX_JOB_RETRY
    if job.kwargs.get('retry_count', 0) < max_retry:
        job.kwargs['retry_count'] += 1
        SCHEDULER.modify_job(job.id, **job.kwargs)
        logger.log(msg=f"Retrying job {job.id} ({job.kwargs['retry_count']} of {max_retry})", level=logging.WARNING)
    else:
        logger.log(msg=(f"Job {job.id} failed after {max_retry} retries", event.exception))

