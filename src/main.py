from fastapi import FastAPI

from src.constants.env import API_PREFIX
from src.db.cache import CACHE
from src.db.database import DATABASE_MANAGER
from user.router import user_router

async def lifespan(app: FastAPI):
    yield
    # close cache connections
    await CACHE.aclose()
    #close database connections
    await DATABASE_MANAGER.aclose_connections()
_app = FastAPI()

middlewares = {}
for middleware in middlewares:
    if isinstance(middleware, tuple):
        _app.add_middleware(middleware[0], **middleware[1])
    else:
        _app.add_middleware(middleware)
routers = [user_router]
for router in routers:
    _app.include_router(router, prefix=f"/{API_PREFIX}")

