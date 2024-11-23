import asyncio
from functools import wraps
from typing import Callable, Any

from constants.env import IS_LOCAL


def extend(cls) -> Callable:
    """
    Add method to non-builtin class.
    Outer function to accept arguments for the decorator
    :param cls: Target class to be extended
    """
    def _decorator(func: Callable) -> Callable:
        """Actual decorator that add function to the class"""
        @wraps(func) # preserve function metadata
        def wrapper():
            """Wrapper function"""
            setattr(cls, func.__name__, func)
        return wrapper
    return _decorator

def pre_run(*funcs: Callable[[], Any]) -> Callable:
    """
    Run functions before calling the decorated function.
    :param funcs: functions that need to be called before calling the decorated function.
    :return: result of the decorated function.
    """
    def _decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args, **kwargs):
            for func in funcs:
                if asyncio.iscoroutinefunction(func):
                    asyncio.run(main=func(), debug=IS_LOCAL)
                else:
                    func()
                return function(*args, **kwargs)
        return wrapper
    return _decorator