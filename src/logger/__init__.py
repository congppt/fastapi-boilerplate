import logging.config

from typing import Any

import sentry_sdk

from config import APP_SETTINGS
from constants import REQUEST_TIMEOUT
from services.discord import DiscordAPI
from utils.formatters import format_exception

NOTIFY_CHANNELS = []


def setup():
    """
    Setup logging services
    """

    if APP_SETTINGS.sentry:
        sentry_config: dict[str, Any] = APP_SETTINGS.sentry.model_dump()
        sentry_sdk.init(
            environment=APP_SETTINGS.env,
            # debug=IS_LOCAL,
            **sentry_config,
        )
    if APP_SETTINGS.discord_api:
        NOTIFY_CHANNELS.append(
            DiscordAPI(
                timeout=REQUEST_TIMEOUT,
                proxy=APP_SETTINGS.proxy,
                verify=False,
                api=APP_SETTINGS.discord_api,
            )
        )
    # Logger Configuration
    logging.config.dictConfig(config=APP_SETTINGS.logging)


async def aomninotify(msg: str):
    """
    Send log message as notification
    """
    if APP_SETTINGS.of_local_env:
        return
    for channel in NOTIFY_CHANNELS:
        if isinstance(channel, DiscordAPI):
            await channel.asend_bot_message(message=msg)


def log(
    msg: str | Exception | tuple[str, Exception],
    level: int | None = None,
    *args,
    **kwargs,
):
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
        exc_msg = format_exception(e=msg[1])
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
