from configparser import ConfigParser

import sentry_sdk
from fastapi import FastAPI

from auth.router import auth_router
from config.router import config_router
from constants.env import CONFIG, SENTRY_DSN, ENV, IS_LOCAL
from middlewares import middlewares
from constants.env import API_PREFIX
from db.cache import CACHE
from db.database import DATABASE_MANAGER
from user.router import user_router


async def astartup():
    config = ConfigParser()
    config.read(CONFIG)
    sentry_config = {key: value for key, value in config.items('Sentry')}
    sentry_sdk.init(dsn=SENTRY_DSN, environment=ENV, debug=IS_LOCAL, **sentry_config)


async def ashutdown():
    # close cache connections
    await CACHE.aclose()
    # close database connections
    await DATABASE_MANAGER.aclose_connections()


async def lifespan(_app: FastAPI):
    await astartup()
    yield
    await ashutdown()


app = FastAPI()

for middleware in middlewares:
    if isinstance(middleware, tuple):
        app.add_middleware(middleware[0], **middleware[1])
    else:
        app.add_middleware(middleware)

routers = [auth_router, user_router, config_router]
for router in routers:
    app.include_router(router, prefix=f"/{API_PREFIX}")


@app.get("/health-check")
async def health_check():
    return "App is running"
