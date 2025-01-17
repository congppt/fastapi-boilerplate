from datetime import timedelta
from typing import Any, Type

from redis.asyncio import StrictRedis

import logger
from utils.serializer import json_deserialize, json_serialize


class CacheSessionManager:
    def __init__(self, url: str):
        self._redis = StrictRedis.from_url(url)
    async def aclose(self):
        """Close all connections including in-use connections."""
        await self._redis.aclose()
        logger.log("All cache connections are closed")

    async def aget(self, key: str, model: Type[Any] = None):
        """
        Get object from cache
        :param key: key used to store object
        :param model: type of object
        :return: deserialized object
        """
        value = await self._redis.get(name=key)
        if value:
            return json_deserialize(json_str=value, model=model)
        return None

    async def aset(self, key: str, value: Any, expire: int | timedelta = None):
        """
        Store object in cache
        :param key: key used to store
        :param value: object to store
        :param expire: object expired after ``expire`` seconds
        """
        value = json_serialize(obj=value)
        await self._redis.set(name=key, value=value, ex=expire)




