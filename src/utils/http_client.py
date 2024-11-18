from collections.abc import Callable
from contextlib import asynccontextmanager
from typing import Any

from httpx import AsyncClient, Request, HTTPStatusError, TimeoutException

class HTTPClient(AsyncClient):
    async def asend(self, request: Request, callback: Callable[..., Any] = None, *callback_args,
                    **callback_kwargs) -> Any:
        response = await self.send(request)
        return callback(response=response, *callback_args, **callback_kwargs) if callback else response

    @asynccontextmanager
    async def astream(self, request: Request, callback: Callable[..., Any] = None, *callback_args,
                      **callback_kwargs) -> Any:
        async with await self.send(request, stream=True) as response:
                yield callback(response=response, *callback_args, **callback_kwargs)