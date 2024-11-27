import asyncio
import importlib
import logging

from typing import Callable, Any, Sequence


class AsyncErrorHandler(logging.Handler):
    """

    """
    def __init__(self, **kwargs):
        super().__init__(level=logging.ERROR)
        funcs = kwargs.get('funcs')
        self._funcs: Sequence[Callable[[str], Any]] = self._resolve_funcs(funcs) or []

    def emit(self, record):
        log_entry = self.format(record)
        # Call the registered functions
        for func in self._funcs:
            asyncio.create_task(func(log_entry))


    @staticmethod
    def _resolve_funcs(funcs: list[Callable[[str], Any] | str]) -> list[Callable[[str], Any]]:
        callables = []
        for func_name in funcs:
            if isinstance(func_name, str):
                module_name, func_name = func_name.rsplit('.', 1)
                module = importlib.import_module(module_name)
                callables.append(getattr(module, func_name))
            else:
                callables.append(func_name)
        return callables