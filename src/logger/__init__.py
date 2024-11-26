import logging

from logging import config
from typing import Any

import sentry_sdk

from config import STARTUP_CONFIG
from constants.env import SENTRY_DSN, ENV, IS_LOCAL
from logger.handler import AsyncErrorHandler
from services import discord
from utils.formatters import format_exception


def setup():
    """
    Setup root logger
    """
    sentry_config: dict[str, Any] = STARTUP_CONFIG.get(section='sentry')
    sentry_sdk.init(dsn=SENTRY_DSN,
                    environment=ENV,
                    # debug=IS_LOCAL,
                    **sentry_config)

    # Logger Configuration
    logging_config: dict[str, Any] = STARTUP_CONFIG.get(section='logging')
    logging.config.dictConfig(config=logging_config)


async def alog_discord(log_entry: str):
    """
    Send log message to discord
    """
    await discord.asend_notification(message=f"`{ENV}` {log_entry}")



def log(msg: object, level: int = logging.INFO, *args, **kwargs):
    """
    Log message
    :param msg: message to log
    :param level: logging level
    :param args: arguments for logging.log
    :param kwargs: keyword arguments. If `duration` (number) keyword exist, append execution time to message.
                   If `request` keyword exist, append keys & items of request to log request
    """
    if isinstance(msg, Exception):
        level = level or logging.ERROR
        msg = format_exception(e=msg)
    adds_up = ""
    duration = kwargs.pop("duration", None)
    if duration:
        adds_up += f"\nDuration: {duration:.2f}s\n"
    request: dict[str, Any] | None = kwargs.pop("request", None)
    if request:
        for key, val in request.items():
            adds_up += f"{key.title()}: {val}\n"
    msg += adds_up
    logging.log(level=level, msg=msg, *args, **kwargs)
