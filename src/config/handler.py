from typing import Any, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import cache
from db.models.system import SystemConfig


async def aget_config(key: str, db: AsyncSession, model: Type[Any] = None) -> Any:
    """
    Get config value from cache & database
    :param key: Config key
    :param db: Database session
    :param model: Type of config value
    :return: config
    """
    value = await cache.aget(key=key, model=model)
    if not value:
        query = select(SystemConfig.value).where(SystemConfig.key == key)
        value = await db.scalar(query)
    return model(**value) if model else value