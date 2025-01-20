import time
from http.client import responses

from fastapi import Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
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
            logger.log(
                msg=f"{(request.client.host if request.client else 'Unknown'):15}  {request.method:8} {request.url.path:32}  {response.status_code:3} {responses[response.status_code]:32} {duration:.2f}s"
            )
        except Exception as e:
            request_data = {
                "client": request.client.host if request.client else "Unknown",
                "method": request.method,
                "path": request.url.path,
                "query": request.query_params,
                "body": body if len(body) < MAX_BODY_LOG else "Large file(s)",
            }
            logger.log(msg=e, request=request_data, duration=duration)
            response = Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(e, ValidationError):
                response = JSONResponse(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    content={
                        "detail": jsonable_encoder(
                            obj=e.errors(include_url=False, include_context=False)
                        )
                    },
                )
        return response
