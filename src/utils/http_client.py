from collections.abc import Callable
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from httpx import AsyncClient, Request, Response


class HTTPClient(AsyncClient):
    async def asend(self,
                    request: Request,
                    callback: Callable[..., Any] | None = None,
                    *callback_args,
                    **callback_kwargs) -> Any:
        """
        Make async HTTP request
        :param request: input data for HTTP call
        :param callback: Callback method runs after receiving response
        :param callback_args: positional arguments for callback
        :param callback_kwargs:
        :return:  response if no callback was given else result of callback
        """
        response: Response | None = None
        try:
            response = await self.send(request)
            if not callback:
                return response
            callback_kwargs = callback_kwargs or {}
            callback_kwargs.update({"response": response})
            return callback(*callback_args, **callback_kwargs) if callback else response
        finally:
            if response: await response.aclose()

    @asynccontextmanager
    async def astream(self,
                      request: Request,
                      callback: Callable[..., Any] = None,
                      *callback_args,
                      **callback_kwargs) -> AsyncGenerator[Any, None]:
        """
        Make async HTTP request
        :param request: input data for HTTP call
        :param callback: Callback method runs after receiving response
        :param callback_args: positional arguments for callback
        :param callback_kwargs: keyword arguments for callback
        :return: response stream if no callback was given else result stream of callback
        """
        response: Response | None = None
        try:
            response: Response = await self.send(request, stream=True)
            if not callback:
                yield response
            callback_kwargs = callback_kwargs or {}
            callback_kwargs.update({"response": response})
            yield callback(response=response, *callback_args, **callback_kwargs) if callback else response
        finally:
            await response.aclose()
