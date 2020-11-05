from asyncio.events import AbstractEventLoop
from typing import List, Union

from .base import BaseResource

__all__ = [
    'MPCResource',
]


class MPCInstrument(object):
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
    def from_dict(cls, data: dict) -> "MPCInstrument":
        return cls(data)


class MPCLinkedEvent(object):
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
    def from_dict(cls, data: dict) -> "MPCLinkedEvent":
        return cls(data)


class MPCResource(BaseResource):
    __slots__ = [
        '_id',
        '_event_time',
        '_link',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(MPCResource, self).__init__(data, loop=loop)
        self._id = data.get("mpcID")
        self._event_time = data.get("eventTime")
        self._link = data.get("link")
        self._data = data

    @property
    def id(self) -> str:
        return self._id

    @property
    def mpcID(self) -> str:
        return self.id

    @property
    def event_time(self) -> str:  # TODO: Implement datetime.datetime
        return self._event_time

    def _process_instruments(self) -> Union[List[MPCInstrument], MPCInstrument, None]:
        if not (instrs := self._data.get("instruments")):
            return None
        elif len(instrs) != 1:
            return [MPCInstrument(data) for data in instrs]
        else:
            return MPCInstrument(instrs[0])

    @property
    def instruments(self) -> Union[List[MPCInstrument], MPCInstrument, None]:
        if (instr := f"{self}instr") not in self._cache:
            self._cache[instr] = self._process_instruments()
        return self._cache[instr]

    def _process_linked_events(self) -> Union[List[MPCLinkedEvent], MPCLinkedEvent, None]:
        if not (le := self._data.get("linkedEvents")):
            return None
        elif len(le) != 1:
            return [MPCLinkedEvent(data) for data in le]
        else:
            return MPCLinkedEvent(le[0])

    @property
    def linked_events(self) -> Union[List[MPCLinkedEvent], MPCLinkedEvent, None]:
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
                  loop: AbstractEventLoop = None) -> "MPCResource":
        return cls(data, loop=loop)
