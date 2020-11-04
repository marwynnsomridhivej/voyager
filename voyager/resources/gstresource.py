from asyncio.events import AbstractEventLoop
from typing import List, Union

from .base import BaseResource

__all__ = [
    'GSTResource',
]


class GSTKPIndex(object):
    __slots__ = [
        '_observed_time',
        '_kp_index',
        '_source',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._observed_time = data.get("observedTime")
        self._kp_index = data.get("kpIndex")
        self._source = data.get("source")
        self._data = data

    @property
    def observed_time(self) -> str:  # TODO: Implement datetime.datetime
        return self._observed_time

    @property
    def kp_index(self) -> int:
        return self._kp_index

    @property
    def source(self) -> str:
        return self._source

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "GSTKPIndex":
        return cls(data)


class GSTLinkedEvent(object):
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
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> None:
        return cls(data)


class GSTResource(BaseResource):
    __slots__ = [
        '_gst_id',
        '_start_time',
        '_link',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(GSTResource, self).__init__(data, loop=loop)
        self._gst_id = data.get("gstID")
        self._start_time = data.get("startTime")
        self._link = data.get("link")
        self._data = data

    @property
    def gst_id(self) -> str:
        return self._gst_id

    @property
    def id(self) -> str:
        return self._gst_id

    @property
    def start_time(self) -> str:  # TODO: Implement datetime.datetime
        return self._start_time

    def _process_kp(self) -> Union[List[GSTKPIndex], GSTKPIndex, None]:
        if not (kp := self._data.get("allKpIndex")):
            return None
        elif len(kp) != 1:
            return [GSTKPIndex(data) for data in kp]
        else:
            return GSTKPIndex(kp[0])

    @property
    def all_kp_index(self) -> Union[List[GSTKPIndex], GSTKPIndex, None]:
        if (kp := f"{self}kpindex") not in self._cache:
            self._cache[kp] = self._process_kp()
        return self._cache[kp]

    def _process_linked_events(self) -> Union[List[GSTLinkedEvent], GSTLinkedEvent, None]:
        if not (le := self._data.get("linkedEvents")):
            return None
        elif len(le) != 1:
            return [GSTLinkedEvent(data) for data in le]
        else:
            return GSTLinkedEvent(le[0])

    @property
    def linked_events(self) -> Union[List[GSTLinkedEvent], GSTLinkedEvent, None]:
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
                  loop: AbstractEventLoop = None) -> "GSTResource":
        return cls(data, loop=loop)
