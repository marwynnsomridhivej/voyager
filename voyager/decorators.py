import asyncio
import datetime
import functools
import weakref
from asyncio.coroutines import iscoroutine, iscoroutinefunction

import asyncstdlib as astd

from .exceptions import MissingDependency


def check_pil_importable(func: callable):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        """Decorator interface to check if the Pillow module can be
        imported

        :param func: the function to decorate
        :type func: callable
        :raises MissingDependency: error raised if Pillow cannot be imported
        :return: the return value of the function
        :rtype: ApodImage
        """
        try:
            import PIL
        except ImportError:
            raise MissingDependency("PIL")
        else:
            return func(*args, **kwargs)
    return decorator


def apply_cache(max_size: int = None):
    def actual_decorator(func: callable):
        if iscoroutine(func) or iscoroutinefunction(func):
            @functools.wraps(func)
            @astd.lru_cache(maxsize=max_size)
            async def deco(*args, **kwargs):
                return await func(*args, **kwargs)
        else:
            @functools.wraps(func)
            @functools.lru_cache(maxsize=max_size)
            def deco(*args, **kwargs):
                return func(*args, **kwargs)
        return deco
    return actual_decorator


class LockManager():
    def __init__(self, lock: asyncio.Lock):
        self.lock = lock
        self._unlockable = True

    def __enter__(self):
        return self

    def defer(self):
        self._unlockable = False

    def __exit__(self):
        if self._unlockable:
            self.lock.release()


class RateLimit(object):
    def __init__(self, max_calls: int = 1000,
                 period: int = 3600, silent_ignore: bool = False) -> None:
        self._max_calls = max_calls
        self._period = period
        self._now = lambda: int(datetime.datetime.now())
        self._silent = silent_ignore
        self._latest_reset = self.now()
        self._calls = 0
        self._locks = weakref.WeakValueDictionary()

    def __call__(self, route):
        def actual_decorator(func):
            @functools.wraps(func)
            async def limiter(*args, **kwargs):
                lock = self._locks.get(route, None)
                if not lock:
                    lock = asyncio.Lock()
                    self._locks[route] = lock
                await lock.acquire()