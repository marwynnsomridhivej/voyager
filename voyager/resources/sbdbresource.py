import datetime
from asyncio.events import AbstractEventLoop
from typing import Generator, List, Union

from ..exceptions import VoyagerException
from .base import BaseResource

__all__ = [
    'SBDBResource',
]


class CADRecord(object):
    __slots__ = [
        '_fc',
        '_des',
        '_orbit_id',
        '_jd',
        '_cd',
        '_dist',
        '_dist_min',
        '_dist_max',
        '_v_rel',
        '_v_inf',
        '_t_sigma_f',
        '_body',
        '_h',
        '_fullname',
    ]
    _FIELDS = [
        'des',
        'orbit_id',
        'jd',
        'cd',
        'dist',
        'dist_min',
        'dist_max',
        'v_rel',
        'v_inf',
        't_sigma_f',
        'body',
        'h',
        'fullname',
    ]
    _cache = {}

    def __init__(self, data: List[str], fields: List[str]) -> None:
        self._fc = self._FIELDS.copy()
        for field, value in zip(fields, data):
            setattr(self, f"_{field}", value)
            self._FIELDS.remove(field)
        for unset in self._FIELDS:
            setattr(self, f"_{unset}", None)

    def __len__(self) -> int:
        if (l := "len") not in self._cache:
            self._cache[l] = len(self._fc) - len(self._FIELDS)
            del self._FIELDS
        return self._cache[l]

    @property
    def des(self) -> Union[str, None]:
        return self._des

    @property
    def orbit_id(self) -> Union[int, None]:
        if not self._orbit_id:
            return None
        return int(self._orbit_id)

    @property
    def jd_time(self) -> Union[float, None]:
        if not self._jd:
            return None
        return float(self._jd)

    @property
    def cd_time(self) -> Union[str, None]:
        return self._cd

    @property
    def cd_datetime(self) -> Union[datetime.datetime, None]:
        if not self._cd:
            return None
        return datetime.datetime.strptime(self._cd, "%Y-%b-%d %H:%M")

    @property
    def dist(self) -> Union[float, None]:
        if not self._dist:
            return None
        return float(self._dist)

    @property
    def dist_min(self) -> Union[float, None]:
        if not self._dist_min:
            return None
        return float(self._dist_min)

    @property
    def dist_max(self) -> Union[float, None]:
        if not self._dist_max:
            return None
        return float(self._dist_max)

    @property
    def v_rel(self) -> Union[float, None]:
        if not self._v_rel:
            return None
        return float(self._v_rel)

    @property
    def v_inf(self) -> Union[float, None]:
        if not self._v_inf:
            return None
        return float(self._v_inf)

    @property
    def t_sigma_f(self) -> Union[str, None]:
        return self._t_sigma_f

    @property
    def body(self) -> Union[str, None]:
        return self._body

    @property
    def h(self) -> Union[float, None]:
        if not self._h:
            return None
        return float(self._h)

    @property
    def abs_mag(self) -> Union[float, None]:
        return self.h

    @property
    def fulname(self) -> Union[str, None]:
        return self._fullname

    def _process_dict(self) -> dict:
        return {field: getattr(self, f"_{field}") for field in self._fc}

    @property
    def to_dict(self) -> dict:
        if self not in self._cache:
            self._cache[self] = self._process_dict()
        return self._cache[self]

    @classmethod
    def from_dict(cls, data: dict) -> "CADRecord":
        if not all((key in cls._FIELDS for key in data)):
            raise VoyagerException("Malformed input. Invalid key(s) supplied")
        return cls([value for value in data.values()], [key for key in data])


class SBDBResource(BaseResource):
    __slots__ = [
        '_signature',
        '_count',
        '_fields',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(SBDBResource, self).__init__(data, loop=loop)
        self._signature = data.get("signature")
        self._count = data.get("count")
        self._fields = data.get("fields")
        self._data = data

    def __len__(self) -> int:
        return self.count

    def __iter__(self):
        return self

    def __next__(self):
        for cr in self.data:
            yield cr

    @property
    def signature(self) -> dict:
        return self._signature

    @property
    def source(self) -> str:
        return self.signature.get("source")

    @property
    def version(self) -> str:
        return self.signature.get("version")

    @property
    def count(self) -> int:
        return int(self._count)

    @property
    def fields(self) -> List[str]:
        return self._fields

    def _process_cad_data(self) -> Union[Generator[CADRecord], CADRecord, None]:
        if not (cad := self._data.get("data")):
            return None
        elif len(cad) != 1:
            for values in cad:
                yield CADRecord(values, self._fields)
        else:
            return CADRecord(cad[0], self._fields)

    @property
    def data(self) -> Union[Generator[CADRecord], CADRecord, None]:
        if self not in self._cache:
            self._cache[self] = self._process_cad_data()
        return self._cache[self]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "SBDBResource":
        return cls(data, loop=loop)
