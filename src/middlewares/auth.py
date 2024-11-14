from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from db.database import aget_db
from src.auth.handler import aauthenticate


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get('Authorization')
        path = request.url.path
        async for db in aget_db():
            user = await aauthenticate(auth_header, path, db)
            request.state.db = db
            request.state.user = user
            return await call_next(request)