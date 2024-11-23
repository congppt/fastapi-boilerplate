import logging
import time

from fastapi import HTTPException, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        client_ip = '127.0.0.1'
        duration = 0.0
        try:
            start = time.perf_counter()
            client_ip = request.client.host
            body = await request.body()
            response = await call_next(request)
            end = time.perf_counter()
            duration = end - start
        except Exception as e:
            if not isinstance(e, HTTPException):
                logging.exception(msg=e, extra={'clientip': client_ip, 'duration': duration})
        finally:
            return response