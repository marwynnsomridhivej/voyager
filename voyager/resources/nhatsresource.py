from asyncio.events import AbstractEventLoop
from typing import Generator, Union

from .base import BaseResource
from .nhat import NHATSData, NHATSignature

__all__ = [
    'NHATSResource',
    'NHATSData',
]


class NHATSResource(BaseResource):
    __slots__ = [
        '_count',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(NHATSResource, self).__init__(data, loop=loop)
        self._count = int(data.get("count"))
        self._data = data

    def __len__(self) -> int:
        return self.count

    @property
    def count(self) -> int:
        return self._count

    @property
    def signature(self) -> NHATSignature:
        if (sig := f"{self}signature") not in self._cache:
            self._cache[sig] = NHATSignature(self._data.get("signature"))
        return self._cache[sig]

    def _process_data(self) -> Union[Generator[NHATSData, None, None], NHATSData, None]:
        if not (dt := self._data.get("data")):
            return None
        elif len(dt) != 1:
            return (NHATSData(data, loop=self._loop) for data in dt)
        else:
            return NHATSData(dt[0], loop=self._loop)

    @property
    def data(self):
        if (dt := f"{self}data") not in self._cache:
            self._cache[dt] = self._process_data()
        return self._cache[dt]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "NHATSResource":
        return cls(data, loop=loop)
