import datetime
from asyncio.events import AbstractEventLoop
from typing import Generator, List, Union

from .base import BaseResource

__all__ = [
    'TLECollection',
    'TLERecord',
]

_ATTRS_RECORD = {
    '@id': str,
    '@type': str,
    'satelliteId': Union[int, str],
    'name': str,
    'date': Union[datetime.datetime, str],
    'line1': str,
    'line2': str,
}
_ATTRS_COLLECTION = {
    '@context': str,
    '@id': str,
    '@type': str,
    'totalItems': Union[int, str],
    'parameters': List[str],
}


class TLERecord(BaseResource):
    __slots__ = [
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(TLERecord, self).__init__(data, loop=loop)
        self._data = data

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "TLERecord":
        return cls(data, loop=loop)


class TLEView(object):
    __slots__ = [
        '_id',
        '_type',
        '_first',
        '_previous',
        '_next',
        '_last',
    ]

    def __init__(self, data: dict) -> None:
        self._id = data.get("@id")
        self._type = data.get("@type")
        self._first = data.get("first")
        self._previous = data.get("previous")
        self._next = data.get("next")
        self._last = data.get("last")

    @property
    def id(self) -> str:
        return self._id

    @property
    def type(self) -> str:
        return self._type

    @property
    def first(self) -> str:
        return self._first

    @property
    def previous(self) -> str:
        return self._previous

    @property
    def next(self) -> str:
        return self._next

    @property
    def last(self) -> str:
        return self._last

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "TLEView":
        return cls(data)


class TLECollection(BaseResource):
    __slots__ = [
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(TLECollection, self).__init__(data, loop=loop)
        self._data = data

    def _process_members(self) -> Union[Generator[TLERecord, None, None], TLERecord, None]:
        if not (mb := self._data.get("member")):
            return None
        elif len(mb) != 1:
            return (TLERecord(data) for data in mb)
        else:
            return TLERecord(mb[0])

    @property
    def members(self) -> Union[Generator[TLERecord, None, None], TLERecord, None]:
        if (mb := f"{self}members") not in self._cache:
            self._cache[mb] = self._process_members()
        return self._cache[mb]

    @property
    def view(self) -> TLEView:
        if (vw := f"{self}view") not in self._cache:
            self._cache[vw] = TLEView(self._data.get("view"))
        return self._cache[vw]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "TLECollection":
        return cls(data, loop=loop)


def _handle(pot_int: str) -> Union[int, str]:
    try:
        return int(pot_int)
    except ValueError:
        return pot_int


def _add_func(_class, name: str, attrdict: dict):
    @property
    def fn(self) -> attrdict.get(name):
        if name not in self._cache:
            self._cache[name] = _handle(self._data.get(name))
        return self._cache[name]
    setattr(_class, name.replace("@", ""), fn)


for attr in _ATTRS_RECORD:
    _add_func(attr)


for attr in _ATTRS_COLLECTION:
    _add_func(attr)
