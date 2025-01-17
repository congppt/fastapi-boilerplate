import asyncio
import importlib
import logging
import os
from datetime import datetime


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


class DailyFileHandler(logging.FileHandler):
    """
    A logging handler that writes log messages to a file named by the current
    date using strftime formatting (e.g. logs/2025/Jan/17.log).
    Each new day will generate a new file (and create directories, if necessary).
    """

    def __init__(self, base_dir: str, encoding: str = "utf8"):
        """
        Create (if not exists) today's file and use it as the stream for logging.
        """
        self._base_dir = base_dir
        now = datetime.now()
        filename = os.path.join(base_dir, now.strftime("%Y\\%b\\%d") + ".log")
        os.makedirs(name=os.path.dirname(p=filename), exist_ok=True)

        logging.FileHandler.__init__(self=self, filename=filename, encoding=encoding)

    def _update_stream(self, record: logging.LogRecord):
        """
        Ensures that we are writing to the correct file for today's date.
        If the day changes, close the old file and open a new one.
        """
        # Example of the directory and filename: logs/2025/January/17.log
        now = datetime.fromtimestamp(record.created)
        filename = os.path.join(self._base_dir, now.strftime("%Y\\%b\\%d") + ".log")
        # If the filename has changed (or none yet), update
        if filename != self.baseFilename:
            # Close the old stream if open
            logging.FileHandler.close(self=self)
            # Ensure that the parent directory exists
            os.makedirs(name=os.path.dirname(p=filename), exist_ok=True)
            # Update state
            self.baseFilename = filename
            logging.FileHandler._open(self=self)

    def emit(self, record: logging.LogRecord):
        self._update_stream(record=record)
        logging.FileHandler.emit(self=self, record=record)
