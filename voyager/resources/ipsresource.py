from asyncio.events import AbstractEventLoop
from typing import List, Union

from .base import BaseResource


__all__ = [
    'IPSResource',
]


class IPSInstrument(object):
    __slots__ = [
        '_id',
        '_display_name',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._id = data.get("id")
        self._display_name = data.get("displayName")
        self._data = data

    @property
    def id(self) -> int:
        return self._id

    @property
    def display_name(self) -> str:
        return self._display_name

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "IPSInstrument":
        return cls(data)


class IPSResource(BaseResource):
    __slots__ = [
        '_catalog',
        '_activity_id',
        '_location',
        '_event_time',
        '_link',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(IPSResource, self).__init__(data, loop=loop)
        self._catalog = data.get("catalog")
        self._activity_id = data.get("activityID")
        self._location = data.get("location")
        self._event_time = data.get("eventTime")
        self._link = data.get("link")
        self._data = data

    @property
    def catalog(self) -> str:
        return self._catalog

    @property
    def activity_id(self) -> str:
        return self._activity_id

    @property
    def location(self) -> str:
        return self._location

    @property
    def event_time(self) -> str:  # TODO: Implement datetime.datetime version
        return self._event_time

    @property
    def link(self) -> str:
        return self._link

    def _process_instruments(self) -> Union[List[IPSInstrument], IPSInstrument, None]:
        if not (instrs := self._data.get("instruments")):
            return None
        elif len(instrs) != 1:
            return [IPSInstrument(data) for data in instrs]
        else:
            return IPSInstrument(instrs[0])

    @property
    def instruments(self) -> Union[List[IPSInstrument], IPSInstrument, None]:
        if self not in self._cache:
            self._cache[self] = self._process_instruments()
        return self._cache[self]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "IPSResource":
        return cls(data, loop=loop)
