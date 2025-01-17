from datetime import timedelta
from typing import Type, Any

from config import APP_SETTINGS
from db.cache import CacheSessionManager
from db.database import DatabaseSessionManager
from db.models.user import User  # noqa: F401
from utils.serializer import json_serialize

DATABASE = DatabaseSessionManager(
    url=APP_SETTINGS.postgres_dsn.unicode_string(),
    pool_size=5,
    max_overflow=10,  # max_overflow + pool_size = max size = 15
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,  # Phát hiện và loại bỏ kết nối chết,
    json_serializer=json_serialize,
)


async def aget_db():
    """Retrieve a database session"""
    async with DATABASE.aget_session() as session:
        yield session


CACHE = CacheSessionManager(url=APP_SETTINGS.redis_dsn.unicode_string())


async def aget_cache(key: str, model: Type[Any] | None = None):
    """
    Get object from cache
    :param key: key used to store object
    :param model: type of object
    :return: deserialized object
    """
    return await CACHE.aget(key=key, model=model)


async def aset_cache(key: str, value: Any, expire: int | timedelta | None = None):
    """
    Store object in cache
    :param key: key used to store
    :param value: object to store
    :param expire: object expired after ``expire`` seconds
    """
    await CACHE.aset(key=key, value=value, expire=expire)
