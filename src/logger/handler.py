import asyncio
import importlib
import logging
from typing import Callable, Any, Sequence


class AsyncErrorHandler(logging.Handler):
    def __init__(self, funcs: Sequence[Callable[[str], Any]], **kwargs):
        super().__init__(level=logging.ERROR)
        if 'funcs' in kwargs:
            funcs = (*funcs, *self._resolve_funcs(kwargs.pop('funcs')))
        self._funcs: tuple[Callable[[str], Any], Any] = funcs

    def emit(self, record):
        log_entry = self.format(record)
        # Call the registered functions
        asyncio.run(self._run_async_if_possible(log_entry))

    async def _run_async_if_possible(self, log_entry):
        """
        Runs all registered functions asynchronously, whether sync or async.
        """
        for func in self._funcs:
            if asyncio.iscoroutinefunction(func):
                await func(log_entry)
            else:
                func(log_entry)

    @staticmethod
    def _resolve_funcs(func_names):
        callables = []
        for func_name in func_names:
            module_name, func_name = func_name.rsplit('.', 1)
            module = importlib.import_module(module_name)
            callables.append(getattr(module, func_name))
        return callables