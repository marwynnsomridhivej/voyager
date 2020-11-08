from asyncio.events import AbstractEventLoop
from typing import Generator, Union

import aiohttp

from .eonetevent import EONETEvent


class EONETSource(object):
    __slots__ = [
        '_id',
        '_title',
        '_url',
        '_link',
        '_data',
        '_loop',
    ]

    def __init__(self, data: dict, loop: AbstractEventLoop) -> None:
        self._id = data.get("id")
        self._title = data.get("title")
        self._url = data.get("url")
        self._link = data.get("link")
        self._data = data
        self._loop = loop

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def url(self) -> str:
        return self._url

    @property
    def link(self) -> str:
        return self._link

    async def _process_events(self) -> Union[Generator[EONETEvent, None, None], EONETEvent, None]:
        async with aiohttp.ClientSession() as cs:
            async with cs.get(self._link) as resp:
                ret = await resp.json()
        if not (events := ret.get("events")):
            return None
        return (EONETEvent(event) for event in events)

    @property
    def events(self) -> Union[Generator[EONETEvent, None, None], EONETEvent, None]:
        if self not in self._cache:
            self._cache[self] = self._loop.run_in_executor(None, self._process_events)
        return self._cache[self]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "EONETSource":
        return cls(data)
