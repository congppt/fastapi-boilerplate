from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from auth.router import auth_router
from config.router import config_router
from middlewares.auth import AuthMiddleware
from middlewares.log import LogMiddleware
from src.constants.env import API_PREFIX
from src.db.cache import CACHE
from src.db.database import DATABASE_MANAGER
from user.router import user_router


async def lifespan(app: FastAPI):
    yield
    # close cache connections
    await CACHE.aclose()
    # close database connections
    await DATABASE_MANAGER.aclose_connections()


_app = FastAPI()

middlewares: set = {
    (CORSMiddleware, {
        "allow_origins": ("*",),
        "allow_methods": ("*",),
        "allow_headers": ("*",),
        "allow_credentials": True,
    }),
    LogMiddleware,
    AuthMiddleware
}
for middleware in middlewares:
    if isinstance(middleware, tuple):
        _app.add_middleware(middleware[0], **middleware[1])
    else:
        _app.add_middleware(middleware)

routers: set = {auth_router, user_router, config_router}
for router in routers:
    _app.include_router(router, prefix=f"/{API_PREFIX}")

