from asyncio.events import AbstractEventLoop
from typing import Union

from .base import BaseResource
from .nasamedia import NASAManifestCollection, NASAMediaCollection

__all__ = [
    'NASALocationResource',
    'NASAMediaResource',
]


class NASALocationResource(BaseResource):
    __slots__ = [
        '_data',
    ]

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(NASALocationResource, self).__init__(data, loop=loop)
        self._data = data

    @property
    def location(self) -> str:
        return self._data.get("location")

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "NASALocationResource":
        return cls(data)


class NASAMediaResource(BaseResource):
    __slots__ = [
        '_col_asset',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(NASAMediaResource, self).__init__(data, loop=loop)
        if data.get("collection_type") == "media":
            self._col_asset = NASAMediaCollection
        else:
            self._col_asset = NASAManifestCollection
        self._data = data

    @property
    def collection(self) -> Union[NASAMediaCollection, NASAManifestCollection, None]:
        if self not in self._cache:
            self._cache[self] = self._col_asset(self._data.get("collection"))
        return self._cache[self]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "NASAMediaResource":
        return cls(data, loop=loop)
