from contextlib import asynccontextmanager
from typing import Sequence

from fastapi import FastAPI

import auth
import config
import user
import workplace
from logger import setup_logger
from middlewares import middlewares
from constants.env import API_PREFIX
from db import CACHE, DATABASE

logger = setup_logger(__name__)
async def astartup():
    logger.info("Application startup")


async def ashutdown():
    # close cache connections
    await CACHE.aclose()
    # close database connections
    await DATABASE.aclose_connections()
    logger.info("Application shutdown")

@asynccontextmanager
async def lifespan(_app: FastAPI):
    await astartup()
    yield
    await ashutdown()


app = FastAPI(lifespan=lifespan)

for middleware in middlewares:
    if isinstance(middleware, Sequence):
        app.add_middleware(middleware[0], **middleware[1])
    else:
        app.add_middleware(middleware)

routers = [auth.router, user.router, config.router, workplace.router]
for router in routers:
    app.include_router(router, prefix=f"/{API_PREFIX}")


@app.get("/health-check")
async def health_check():
    return "App is running"
