from asyncio.events import AbstractEventLoop
from collections import namedtuple
from typing import Generator, List, Union

from .base import BaseResource
from .missiondesign import (MissionDesignDVLowThrust, MissionDesignObject,
                            MissionDesignSignature)

__all__ = [
    'MissionDesignResource',
]


_SELM = namedtuple("SelectedMission", [
    "MJD0",
    "MJDf",
    "vinf_dep",
    "vinf_arr",
    "phase_ang",
    "earth_dist",
    "elong_arr",
    "decl_dep",
    "approach_ang",
    "tof",
])

_ATTRS = {
    "tof": Union[List[float], None],
    "dep_date": Union[List[float], None],
    "vinf_dep": Union[List[List[float]], None],
    "vinf_arr": Union[List[List[float]], None],
    "phase_ang": Union[List[List[float]], None],
    "earth_dist": Union[List[List[float]], None],
    "elong_arr": Union[List[List[float]], None],
    "decl_dep": Union[List[List[float]], None],
    "approach_ang": Union[List[List[float]], None],
}


class MissionDesignResource(BaseResource):
    __slots__ = [
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(MissionDesignResource, self).__init__(data, loop=loop)
        self._data = data

    @property
    def signature(self) -> MissionDesignSignature:
        if (sig := f"{self}signature") not in self._cache:
            self._cache[sig] = MissionDesignSignature(self._data.get("signature"))
        return self._cache[sig]

    @property
    def object(self) -> MissionDesignObject:
        if (obj := f"{self}object") not in self._cache:
            self._cache[obj] = MissionDesignObject(self._data.get("object"))
        return self._cache[obj]

    @property
    def dv_lowthrust(self) -> MissionDesignDVLowThrust:
        if (lt := f"{self}lt") not in self._cache:
            self._cache[lt] = MissionDesignDVLowThrust(self._data.get("dv_lowthrust"))
        return self._cache[lt]

    @property
    def fields(self) -> Union[List[str], None]:
        if (fd := f"{self}fields") not in self._cache:
            self._cache[fd] = self._data.get("fields")
        return self._cahe[fd]

    def _process_sm(self) -> Union[Generator[namedtuple, None, None], namedtuple, None]:
        if not (sm := self._data.get("selectedMissions")):
            return None
        elif len(sm) != 1:
            return (_SELM(*data) for data in sm)
        else:
            return _SELM(*sm[0])

    @property
    def selected_missions(self) -> Union[Generator[namedtuple, None, None], namedtuple, None]:
        if (sm := f"{self}sm") not in self._cache:
            self._cache[sm] = self._process_sm()
        return self._cache[sm]

    @property
    def missions(self) -> Union[Generator[namedtuple, None, None], namedtuple, None]:
        return self.selected_missions

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "MissionDesignResource":
        return cls(data, loop=loop)


def _add_func(name: str):
    @property
    def fn(self) -> _ATTRS.get(name):
        return self._data.get(name)
    setattr(MissionDesignResource, name, fn)


for attr in _ATTRS:
    _add_func(attr)
