from contextlib import asynccontextmanager

from fastapi import FastAPI

import auth
import config
import user
import logger
from config import APP_SETTINGS
from logger import NOTIFY_CHANNELS
from middlewares import middlewares
from db import CACHE, DATABASE


async def astartup():
    logger.setup()
    logger.log(msg="----------------Application start-------------------")

async def ashutdown():
    # close cache connections
    await CACHE.aclose()
    # shutdown job scheduler
    # close database connections
    await DATABASE.aclose_connections()
    logger.log(msg="---------------Application shutdown------------------")
    [channel.aclose() for channel in NOTIFY_CHANNELS]

@asynccontextmanager
async def lifespan(_app: FastAPI):
    await astartup()
    yield
    await ashutdown()

app = FastAPI(lifespan=lifespan)

for middleware in middlewares:
    if isinstance(middleware, tuple):
        app.add_middleware(middleware[0], **middleware[1])
    else:
        app.add_middleware(middleware)

routers = [auth.router, user.router, config.router]
for router in routers:
    app.include_router(router, prefix=f"/{APP_SETTINGS.api_prefix}")


@app.get("/health-check", summary="Health check")
async def health_check():
    return "App is running"

@app.get("/exception", summary="Raise exception")
async def raise_exception():
    raise ValueError("Something went wrong")