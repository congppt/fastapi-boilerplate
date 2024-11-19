from fastapi import FastAPI

from auth.router import auth_router
from config.router import config_router
from middlewares import middlewares
from src.constants.env import API_PREFIX
from src.db.cache import CACHE
from src.db.database import DATABASE_MANAGER
from user.router import user_router


async def lifespan(_app: FastAPI):
    yield
    # close cache connections
    await CACHE.aclose()
    # close database connections
    await DATABASE_MANAGER.aclose_connections()


app = FastAPI()


for middleware in middlewares:
    if isinstance(middleware, tuple):
        app.add_middleware(middleware[0], **middleware[1])
    else:
        app.add_middleware(middleware)

routers: set = {auth_router, user_router, config_router}
for router in routers:
    app.include_router(router, prefix=f"/{API_PREFIX}")

@app.get("/health-check")
async def health_check():
    return "App is running"