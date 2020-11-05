from asyncio.events import AbstractEventLoop
from typing import List, Union

from .base import BaseResource

__all__ = [
    'HSSResource',
]


class HSSInstrument(object):
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
    def from_dict(cls, data: dict) -> "HSSInstrument":
        return cls(data)


class HSSLinkedEvent(object):
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
    def from_dict(cls, data: dict) -> "HSSLinkedEvent":
        return cls(data)


class HSSResource(BaseResource):
    __slots__ = [
        '_id',
        '_event_time',
        '_link',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(HSSResource, self).__init__(data, loop=loop)
        self._id = data.get("hssID")
        self._event_time = data.get("eventTime")
        self._link = data.get("link")
        self._data = data

    @property
    def id(self) -> str:
        return self._id

    @property
    def hssID(self) -> str:
        return self.id

    @property
    def event_time(self) -> str:  # TODO: Implement datetime.datetime
        return self._event_time

    def _process_instruments(self) -> Union[List[HSSInstrument], HSSInstrument, None]:
        if not (instrs := self._data.get("instruments")):
            return None
        elif len(instrs) != 1:
            return [HSSInstrument(data) for data in instrs]
        else:
            return HSSInstrument(instrs[0])

    @property
    def instruments(self) -> Union[List[HSSInstrument], HSSInstrument, None]:
        if (instr := f"{self}instr") not in self._cache:
            self._cache[instr] = self._process_instruments()
        return self._cache[instr]

    def _process_linked_events(self) -> Union[List[HSSLinkedEvent], HSSLinkedEvent, None]:
        if not (le := self._data.get("linkedEvents")):
            return None
        elif len(le) != 1:
            return [HSSLinkedEvent(data) for data in le]
        else:
            return HSSLinkedEvent(le[0])

    @property
    def linked_events(self) -> Union[List[HSSLinkedEvent], HSSLinkedEvent, None]:
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
                  loop: AbstractEventLoop = None) -> "HSSResource":
        return cls(data, loop=loop)
