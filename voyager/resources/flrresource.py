from asyncio.events import AbstractEventLoop
from typing import List, Union

from .base import BaseResource


__all__ = [
    'FLRResource',
]


class FLRInstrument(object):
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
    def from_dict(cls, data: dict) -> "FLRInstrument":
        return cls(data)


class FLRLinkedEvent(object):
    __slots__ = [
        '_activity_id',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._activity_id = data.get("activityID")
        self._data = data

    @property
    def activity_id(self) -> str:
        return self._activity_id

    @property
    def id(self) -> str:
        return self.activity_id

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "FLRLinkedEvent":
        return cls(data)


class FLRResource(BaseResource):
    __slots__ = [
        '_id',
        '_begin_time',
        '_peak_time',
        '_end_time',
        '_class_type',
        '_source_location',
        '_active_region_num',
        '_link',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(FLRResource, self).__init__(data, loop=loop)
        self._id = data.get("flrID")
        self._begin_time = data.get("beginTime")
        self._peak_time = data.get("peakTime")
        self._end_time = data.get("endTime")
        self._class_type = data.get("classType")
        self._source_location = data.get("sourceLocation")
        self._active_region_num = data.get("activeRegionNum")
        self._link = data.get("link")
        self._data = data

    @property
    def id(self) -> str:
        return self._id

    @property
    def flrID(self) -> str:
        return self.id

    def _process_instruments(self) -> Union[List[FLRInstrument], FLRInstrument, None]:
        if not (instrs := self._data.get("instruments")):
            return None
        elif len(instrs) != 1:
            return [FLRInstrument(data) for data in instrs]
        else:
            return FLRInstrument(instrs[0])

    @property
    def instruments(self) -> Union[List[FLRInstrument], FLRInstrument, None]:
        if (instrs := f"{self}instrs") not in self._cache:
            self._cache[instrs] = self._process_instruments()
        return self._cache[instrs]

    @property
    def begin_time(self) -> str:
        return self._begin_time

    @property
    def peak_time(self) -> str:
        return self._peak_time

    @property
    def end_time(self) -> str:
        return self._end_time

    @property
    def class_type(self) -> str:
        return self._class_type

    @property
    def source_location(self) -> str:
        return self._source_location

    @property
    def active_region_num(self) -> int:
        return self._active_region_num

    def _process_linked_events(self) -> Union[List[FLRLinkedEvent], FLRLinkedEvent, None]:
        if not (le := self._data.get("linkedEvents")):
            return None
        elif len(le) != 1:
            return [FLRLinkedEvent(data) for data in le]
        else:
            return FLRLinkedEvent(le[0])

    @property
    def linked_events(self) -> Union[List[FLRLinkedEvent], FLRLinkedEvent, None]:
        if (le := f"{self}le") not in self._cache:
            self._cache[le] = self._process_linked_events()
        return self._cache[le]

    @property
    def link(self) -> str:
        return self._link

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "FLRResource":
        return cls(data, loop=loop)
