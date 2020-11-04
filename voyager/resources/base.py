import asyncio
from asyncio.events import AbstractEventLoop, AbstractEventLoopPolicy
from typing import Union


__all__ = [
    'BaseResource',
]


class BaseResource(object):
    __slots__ = [
        '_query_url',
        '_code',
        '_loop',
        '_attrs',
    ]

    def __init__(self, attrs: dict, loop: AbstractEventLoop = None) -> None:
        self._query_url = attrs.get("query_url", None)
        self._code = attrs.get("code", 200)
        if not loop:
            try:
                self._loop = asyncio.get_running_loop()
            except RuntimeError:
                self._loop = asyncio.get_event_loop()
        else:
            self._loop = loop
        self._data = attrs

    @property
    def query_url(self) -> Union[str, None]:
        return self._query_url

    @property
    def code(self) -> int:
        return self._code

    @property
    def loop(self) -> AbstractEventLoop:
        return self._loop

    @loop.setter
    def loop(self, new_loop: AbstractEventLoop) -> None:
        self._loop = new_loop

    def set_event_loop_policy(self, policy: AbstractEventLoopPolicy) -> None:
        asyncio.set_event_loop_policy(policy)

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "BaseResource":
        return cls(data, loop=loop)
