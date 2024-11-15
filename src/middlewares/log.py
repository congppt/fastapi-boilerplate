import time

from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            start = time.perf_counter()
            client_ip = request.client.host
            body = await request.body()
            response = await call_next(request)
            end = time.perf_counter()
            duration = end - start
        except Exception as e:
            if not isinstance(e, HTTPException):
                pass
        finally:
            return response