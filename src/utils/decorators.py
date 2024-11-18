from functools import wraps
from typing import Callable


def extend(cls):
    """
    Add method to class.
    Outer function to accept arguments for the decorator
    :param cls: Target class to be extended
    """
    def _decorator(func: Callable):
        """Actual decorator that add function to the class"""
        @wraps(func) # preserve function metadata
        def wrapper():
            """Wrapper function"""
            setattr(cls, func.__name__, func)
    return _decorator