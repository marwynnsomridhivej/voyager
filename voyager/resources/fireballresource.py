import datetime
from asyncio.events import AbstractEventLoop
from typing import Generator, List, Union

from ..exceptions import VoyagerException
from .base import BaseResource

__all__ = [
    'FireballResource',
]


class FireballRecord(object):
    __slots__ = [
        '_fc',
        '_date',
        '_lat',
        '_lon',
        '_lat_dir',
        '_lon_dir',
        '_alt',
        '_vel',
        '_energy',
        '_impact_e',
        '_vx',
        '_vy',
        '_vz',
    ]
    _FIELDS = [
        'date',
        'lat',
        'lon',
        'lat-dir',
        'lon-dir',
        'alt',
        'vel',
        'energy',
        'impact-e',
        'vx',
        'vy',
        'vz',
    ]
    _cache = {}

    def __init__(self, data: List[str], fields: List[str]) -> None:
        self._fc = self._FIELDS.copy()
        for field, value in zip(fields, data):
            setattr(self, f"_{field.replace('-', '_')}", value)
            self._FIELDS.remove(field)
        for unset in self._FIELDS:
            setattr(self, f"_{unset.replace('-', '_')}", None)

    def __len__(self) -> int:
        if (l := "len") not in self._cache:
            self._cache[l] = len(self._fc) - len(self._FIELDS)
            del self._FIELDS
        return self._cache[l]

    @property
    def date(self) -> Union[str, None]:
        return self._date

    @property
    def datetime(self) -> Union[datetime.datetime, None]:
        if not self._date:
            return None
        return datetime.datetime.strptime(self._date, "%Y-%m-%d %H:%M:%S")

    @property
    def lat(self) -> Union[float, None]:
        if not self._lat:
            return None
        return float(self._lat)

    @property
    def latitude(self) -> Union[float, None]:
        return self.lat

    @property
    def lon(self) -> Union[float, None]:
        if not self._lon:
            return None
        return float(self._lon)

    @property
    def longitude(self) -> Union[float, None]:
        return self.lon

    @property
    def lat_dir(self) -> Union[str, None]:
        return self._lat_dir

    @property
    def latitude_dir(self) -> Union[str, None]:
        return self.lat_dir

    @property
    def lon_dir(self) -> Union[str, None]:
        return self._lon_dir

    @property
    def longitude_dir(self) -> Union[str, None]:
        return self.lon_dir

    @property
    def alt(self) -> Union[float, None]:
        if not self._alt:
            return None
        return float(self._alt)

    @property
    def altitude(self) -> Union[float, None]:
        return self.alt

    @property
    def vel(self) -> Union[float, None]:
        if not self._vel:
            return None
        return float(self._vel)

    @property
    def velocity(self) -> Union[float, None]:
        return self.vel

    @property
    def energy(self) -> Union[float, None]:
        if not self._energy:
            return None
        return float(self._energy)

    @property
    def impact_e(self) -> Union[float, None]:
        if not self._impact_e:
            return None
        return float(self._impact_e)

    @property
    def impact_energy(self) -> Union[float, None]:
        return self.impact_e

    @property
    def vx(self) -> Union[float, None]:
        if not self._vx:
            return None
        return float(self._vx)

    @property
    def velocity_x(self) -> Union[float, None]:
        return self.vx

    @property
    def vy(self) -> Union[float, None]:
        if not self._vy:
            return None
        return float(self._vy)

    @property
    def velocity_y(self) -> Union[float, None]:
        return self.vy

    @property
    def vz(self) -> Union[float, None]:
        if not self._vz:
            return None
        return self._vz

    @property
    def velocity_z(self) -> Union[float, None]:
        return self.vz

    def _process_dict(self) -> dict:
        return {field: getattr(self, f"_{field.replace('-', '_')}") for field in self._fc}

    @property
    def to_dict(self) -> dict:
        if self not in self._cache:
            self._cache[self] = self._process_dict()
        return self._cache[self]

    @classmethod
    def from_dict(cls, data: dict) -> "FireballRecord":
        if not all((key in cls._FIELDS for key in data)):
            raise VoyagerException("Malformed input. Invalid key(s) supplied")
        return cls([value for value in data.values()], [key for key in data])


class FireballResource(BaseResource):
    __slots__ = [
        '_signature',
        '_count',
        '_fields',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(FireballResource, self).__init__(data, loop=loop)
        self._signature = data.get("signature")
        self._count = data.get("count")
        self._fields = data.get("fields")
        self._data = data

    def __len__(self) -> int:
        return self.count

    def __iter__(self):
        return self

    def __next__(self):
        for fb in self.data:
            yield fb

    @property
    def signature(self) -> str:
        return self._signature

    @property
    def source(self) -> str:
        return self._signature.get("source")

    @property
    def version(self) -> str:
        return self._signature.get("version")

    @property
    def count(self) -> int:
        return int(self._count)

    @property
    def fields(self) -> List[str]:
        return self._fields

    def _process_fb_data(self) -> Union[Generator[FireballRecord, None, None], FireballRecord, None]:
        if not (fb := self._data.get("data")):
            return None
        elif len(fb) != 1:
            for values in fb:
                yield FireballRecord(values, self._fields)
        else:
            return FireballRecord(fb[0], self._fields)

    @property
    def data(self) -> Union[Generator[FireballRecord, None, None], FireballRecord, None]:
        if self not in self._cache:
            self._cache[self] = self._process_fb_data()
        return self._cache[self]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "FireballResource":
        return cls(data, loop=loop)
