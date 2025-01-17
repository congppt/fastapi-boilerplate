import asyncio
import importlib
import logging
from datetime import time

from logging.handlers import TimedRotatingFileHandler

from typing import Callable, Any, Sequence


class AsyncErrorHandler(logging.Handler):
    """ """

    def __init__(self, **kwargs):
        super().__init__(level=logging.ERROR)
        funcs: list[Callable[[str], Any] | str] = kwargs.get("funcs", [])
        self._funcs: Sequence[Callable[[str], Any]] = self._resolve_funcs(funcs=funcs)

    def emit(self, record):
        log_entry = self.format(record=record)
        # Call the registered functions
        for func in self._funcs:
            asyncio.create_task(coro=func(log_entry))

    @staticmethod
    def _resolve_funcs(funcs: list[Callable[[str], Any] | str]):
        callables: list[Callable[[str], Any]] = []
        for func_name in funcs:
            if isinstance(func_name, str):
                module_name, func_name = func_name.rsplit(sep=".", maxsplit=1)
                module = importlib.import_module(name=module_name)
                callables.append(getattr(module, func_name))
            else:
                callables.append(func_name)
        return callables


class DailyRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(
        self,
        filename: str,
        when: str = "midnight",
        interval: int = 1,
        backupCount: int = 7,
        encoding: str | None = None,
        delay: bool = False,
        utc: bool = False,
        atTime: time | None = None,
        **kwargs,
    ):
        super().__init__(
            filename=filename,
            when=when,
            interval=interval,
            backupCount=backupCount,
            encoding=encoding,
            delay=delay,
            utc=utc,
            atTime=atTime,
            **kwargs,
        )
