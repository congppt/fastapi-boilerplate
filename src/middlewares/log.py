import time
from http.client import responses

from fastapi import Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

import logger
from constants import MAX_BODY_LOG

class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        duration = 0.0
        body = await request.body()
        try:
            response = await call_next(request)
            end = time.perf_counter()
            duration = end - start
            msg= f'{request.client.host:15} - {request.method} {request.url.path} - {response.status_code} {responses[response.status_code]} {duration:.2f}s'
            logger.log(msg)
        except Exception as e:
            msg = e
            request_data = {
                'client_ip': request.client.host,
                'method': request.method,
                'path': request.url.path,
                'query': request.query_params,
                'body': body if len(body) < MAX_BODY_LOG else 'Large file(s)',
            }
            response = Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            logger.log(msg=msg, request=request_data, duration=duration)
        return response