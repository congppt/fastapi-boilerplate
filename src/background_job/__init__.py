from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db import DATABASE

JOB_STORES = {
    'default': SQLAlchemyJobStore(engine=DATABASE.engine)
}
SCHEDULER = AsyncIOScheduler(jobstores=JOB_STORES)