from apscheduler.events import EVENT_JOB_ERROR
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from background_job.handler import listen_job_execute_error
from db import DATABASE

__JOB_STORES = {
    'default': SQLAlchemyJobStore(engine=DATABASE.engine)
}
SCHEDULER = AsyncIOScheduler(jobstores=__JOB_STORES)
SCHEDULER.add_listener(listen_job_execute_error, EVENT_JOB_ERROR)