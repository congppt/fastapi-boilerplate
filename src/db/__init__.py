from collections.abc import AsyncGenerator
from datetime import timedelta
from typing import Type, Any

from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from constants.env import DB_URL, REDIS_URL
from utils.json_handler import json_serialize
from .cache import CacheSessionManager
from .database import DatabaseSessionManager
from .models.student import *
from .models.user import *

DATABASE = DatabaseSessionManager(
    url=DB_URL,
    pool_size=5,
    max_overflow=10,  # max_overflow + pool_size = max size = 15
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,  # Phát hiện và loại bỏ kết nối chết,
    json_serializer=json_serialize)

async def aget_db() -> AsyncGenerator[AsyncSession, None]:
    """Retrieve a database session"""
    async with DATABASE.aget_session() as session:
        yield session

JOB_STORES = {
    'default': SQLAlchemyJobStore(engine=DATABASE.engine)
}

CACHE = CacheSessionManager(REDIS_URL)

async def aget(key: str, model: Type[Any] = None):
    """
        Get object from cache
        :param key: key used to store object
        :param model: type of object
        :return: deserialized object
    """
    return await CACHE.aget(key=key, model=model)

async def aset(key: str, value: Any, expire: int | timedelta = None):
    """
        Store object in cache
        :param key: key used to store
        :param value: object to store
        :param expire: object expired after ``expire`` seconds
    """
    await CACHE.aset(key=key, value=value, expire=expire)
