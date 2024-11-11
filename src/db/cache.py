from datetime import timedelta
from typing import Any, Type

from redis.asyncio import StrictRedis

from src.constants.env import REDIS_URL
from src.helpers.json_handler import json_deserialize, json_serialize

CACHE = StrictRedis.from_url(REDIS_URL)

async def aget(key: str, model: Type[Any] = None):
    """Get object from cache"""
    value = await CACHE.get(key)
    return json_deserialize(value, model)

async def aset(key: str, value: Any, expire: int | timedelta = None):
    """Store object in cache"""
    value = json_serialize(value)
    await CACHE.set(key, value, expire)

