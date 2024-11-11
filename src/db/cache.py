from datetime import timedelta
from typing import Any, Type

from redis.asyncio import StrictRedis

from src.constants.env import REDIS_URL
from src.utils.json_handler import json_deserialize, json_serialize


class __CacheSessionManager:
    def __init__(self, url: str) -> None:
        self._redis = StrictRedis.from_url(url)
    async def aclose(self) -> None:
        """Close all connections including in-use"""
        await self._redis.aclose()

    async def aget(self, key: str, model: Type[Any] = None):
        """Get object from cache"""
        value = await self._redis.get(key)
        return json_deserialize(value, model)

    async def aset(self, key: str, value: Any, expire: int | timedelta = None):
        """Store object in cache"""
        value = json_serialize(value)
        await self._redis.set(key, value, expire)

CACHE = __CacheSessionManager(REDIS_URL)

async def aget(key: str, model: Type[Any] = None):
    """Get object from cache"""
    return await CACHE.aget(key, model)

async def aset(key: str, value: Any, expire: int | timedelta = None):
    """Store object in cache, expire after ``expire`` seconds if set"""
    await CACHE.aset(key, value, expire)



