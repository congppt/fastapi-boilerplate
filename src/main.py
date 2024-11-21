from configparser import ConfigParser
from typing import Sequence

import sentry_sdk
from fastapi import FastAPI

import auth
import config
import user
from constants.env import CONFIG, SENTRY_DSN, ENV, IS_LOCAL
from middlewares import middlewares
from constants.env import API_PREFIX
from db import CACHE, DATABASE


async def astartup():
    _config = ConfigParser()
    _config.read(CONFIG)
    sentry_config = {key: value for key, value in _config.items('Sentry')}
    sentry_sdk.init(dsn=SENTRY_DSN, environment=ENV, debug=IS_LOCAL, **sentry_config)


async def ashutdown():
    # close cache connections
    await CACHE.aclose()
    # close database connections
    await DATABASE.aclose_connections()


async def lifespan(_app: FastAPI):
    await astartup()
    yield
    await ashutdown()


app = FastAPI()

for middleware in middlewares:
    if isinstance(middleware, Sequence):
        app.add_middleware(middleware[0], **middleware[1])
    else:
        app.add_middleware(middleware)

routers = [auth.router, user.router, config.router]
for router in routers:
    app.include_router(router, prefix=f"/{API_PREFIX}")


@app.get("/health-check")
async def health_check():
    return "App is running"
