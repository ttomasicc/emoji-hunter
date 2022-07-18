__author__ = "Tin Tomašić"

from functools import wraps
from typing import Callable


def coroutine(func) -> Callable:
    """ Utility decorator which wraps the start of coroutine generator

    Returns
    -------
    Callable - started coroutine
    """
    @wraps(func)
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr

    return start
