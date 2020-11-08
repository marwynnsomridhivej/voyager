from asyncio.events import AbstractEventLoop
from typing import Generator, Union

import aiohttp

from .eonetlayer import EONETLayer


class EONETCategory(object):
    __slots__ = [
        '_id',
        '_title',
        '_link',
        '_description',
        '_data',
        '_loop',
    ]
    _cache = {}

    def __init__(self, data: dict, loop: AbstractEventLoop) -> None:
        self._id = data.get("id")
        self._title = data.get("title")
        self._link = data.get("link")
        self._description = data.get("description")
        self._layers = data.get("layers")
        self._data = data
        self._loop = loop

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def link(self) -> str:
        return self._link

    @property
    def description(self) -> str:
        return self._description

    async def _process_layers(self) -> Union[Generator[EONETLayer, None, None], EONETLayer, str, None]:
        async with aiohttp.ClientSession() as cs:
            async with cs.get(self._layers) as resp:
                ret = await resp.json()
        if not (cat := ret.get("categories")):
            return None
        if len(cat) != 1:
            return self._layers
        if len((lyr := cat[0].get("layers"))) != 1:
            return (EONETLayer(data) for data in lyr)
        return EONETLayer(lyr[0])

    @property
    def layers(self) -> str:
        if self not in self._cache:
            self._cache[self] = self._loop.run_in_executor(None, self._process_layers)
        return self._cache[self]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "EONETCategory":
        return cls(data)
