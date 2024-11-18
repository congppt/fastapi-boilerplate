from datetime import timedelta
from typing import Any, Type

from redis.asyncio import StrictRedis

from src.constants.env import REDIS_URL
from src.utils.json_handler import json_deserialize, json_serialize


class CacheSessionManager:
    def __init__(self, url: str) -> None:
        self._redis = StrictRedis.from_url(url)
    async def aclose(self) -> None:
        """Close all connections including in-use connections."""
        await self._redis.aclose()

    async def aget(self, key: str, model: Type[Any] = None):
        """
        Get object from cache
        :param key: key used to store object
        :param model: type of object
        :return: deserialized object
        """
        value = await self._redis.get(name=key)
        return json_deserialize(json_str=value, model=model)

    async def aset(self, key: str, value: Any, expire: int | timedelta = None) -> None:
        """
        Store object in cache
        :param key: key used to store
        :param value: object to store
        :param expire: object expired after ``expire`` seconds
        """
        value = json_serialize(obj=value)
        await self._redis.set(name=key, value=value, ex=expire)

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



