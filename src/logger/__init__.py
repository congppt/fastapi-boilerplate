import logging
from logging import config
from typing import Any

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from config import STARTUP_CONFIG
from constants.env import SENTRY_DSN, ENV, IS_LOCAL
from logger.handler import AsyncErrorHandler
from services import discord


def setup_logger():
    sentry_config: dict[str, Any] = STARTUP_CONFIG.get(section='sentry')
    sentry_sdk.init(dsn=SENTRY_DSN,
                    environment=ENV,
                    #debug=IS_LOCAL,
                    # integrations=[StarletteIntegration(),
                    #               FastApiIntegration()],
                    **sentry_config)

    # Logger Configuration
    logging_config: dict[str, Any] = STARTUP_CONFIG.get(section='logging')
    logging.config.dictConfig(config=logging_config)

async def alog_discord(log_entry: str):
    await discord.asend_notification(message=f"`{ENV}` {log_entry}")
