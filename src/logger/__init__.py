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



def log(msg: object, level: int = None, *args, **kwargs):
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
    elif isinstance(msg, tuple):
        level = level or logging.ERROR
        exc_msg = format_exception(msg[1])
        msg = msg[0] + exc_msg
    else:
        level = level or logging.INFO
    adds_up = ""
    duration = kwargs.pop("duration", None)
    if duration:
        adds_up += f"\n**Duration**: {duration:.2f}s"
    request: dict[str, Any] | None = kwargs.pop("request", None)
    if request:
        for key, val in request.items():
            adds_up += f"\n{key.title():6}: {val}"
    msg += adds_up
    logging.log(level=level, msg=msg, *args, **kwargs)
