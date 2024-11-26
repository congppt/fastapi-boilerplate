import logging
from typing import Any, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from constants.env import ENV
from db import aget_cache
from db.models.system import SystemConfig
from utils.parser import parse
from utils.serializer import json_deserialize, json_parse


async def aget_config(key: str, db: AsyncSession, model: Type[Any] = None) -> Any:
    """
    Get config value from cache & database
    :param key: Config key
    :param db: Database session
    :param model: Type of config value
    :return: config
    """
    value = await aget_cache(key=key, model=model)
    if not value:
        query = select(SystemConfig.value).where(SystemConfig.key == key)
        value = await db.scalar(query)
    return model(**value) if model else value

class StartupConfig:
    """
    Load app config from .json file
    """
    def __init__(self, filename: str):
        self._cache: dict[tuple[str, Any], Any] = {}
        path = filename + '.json'
        with open(path, 'r') as file:
            self._config: dict = json_deserialize(file.read())
        try:
            ext_path = filename + f'{ENV}' + '.json'
            with open(ext_path, 'r') as file:
                override_config: dict = json_deserialize(file.read())
                self._config.update(override_config)
        except FileNotFoundError:
            logging.warning('Specific environment config was not given')

    def get(self, section: str, model: Type[Any] = None) -> Any:
        """
        Retrieve config object (dict[str, str] or  if model given) from .ini file specified in environment
        :param section: Section name
        :param model: Type of config value
        :return: config value
        """
        # check cache
        kwargs = self._cache.get((section, model)) or self._config.get(section)
        if not model:
            # cache value
            self._cache[(section, None)] = kwargs
            return kwargs
        instance = parse(value=kwargs, model=model, hook=json_parse)
        self._cache[(section, model)] = instance
        return instance

