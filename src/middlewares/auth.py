from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from auth.handler import acheck_permission
from db.database import aget_db
from src.auth.handler import aget_request_user


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get('Authorization')
        path = request.url.path
        async for db in aget_db():
            user = await aget_request_user(auth_header, db)
            await acheck_permission(user, path)
            request.state.db = db
            request.state.user = user
            return await call_next(request)