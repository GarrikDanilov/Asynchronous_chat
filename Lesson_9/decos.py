import inspect
import time
from functools import wraps
from typing import Any


def log(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            caller_frame = inspect.currentframe().f_back
            caller_name = caller_frame.f_code.co_name
            logger.debug(f'Вызвана функция {func.__name__} с аргументами {args}, {kwargs}.\n  '
                         f'Вызов из модуля {inspect.getmodulename(inspect.getfile(func))}.\n  '
                         f'Функция {func.__name__} вызвана из функции {caller_name}.')
            return res
        return wrapper
    return decorator


class Log():
    def __init__(self, logger):
        self.logger = logger

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            caller_frame = inspect.currentframe().f_back
            caller_name = caller_frame.f_code.co_name
            self.logger.debug(f'Вызвана функция {func.__name__} с аргументами {args}, {kwargs}.\n  '
                         f'Вызов из модуля {inspect.getmodulename(inspect.getfile(func))}.\n  '
                         f'Функция {func.__name__} вызвана из функции {caller_name}.')
            return res
        return wrapper
    