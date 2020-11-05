from asyncio.events import AbstractEventLoop
from typing import List, Union
from .base import BaseResource
import datetime


class MarsCamera(object):
    __slots__ = [
        '_id',
        '_name',
        '_rover_id',
        '_full_name',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._id = data.get("id")
        self._name = data.get("name")
        self._rover_id = data.get("rover_id")
        self._full_name = data.get("full_name")
        self._data = data

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def rover_id(self) -> int:
        return self._rover_id

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "MarsCamera":
        return cls(data)


class MarsRover(object):
    __slots__ = [
        '_id',
        '_name',
        '_landing_date',
        '_launch_date',
        '_status',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._id = data.get("id")
        self._name = data.get("name")
        self._landing_date = data.get("landing_date")
        self._launch_date = data.get("launch_date")
        self._status = data.get("status")
        self._data = data

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def landing_date(self) -> str:
        return self._landing_date

    @property
    def landing_datetime(self) -> datetime.datetime:
        return datetime.datetime.strptime(self._landing_date, "%Y-%m-%d")

    @property
    def launch_date(self) -> str:
        return self._launch_date

    @property
    def launch_datetime(self) -> datetime.datetime:
        return datetime.datetime.strptime(self._launch_date, "%Y-%m-%d")

    @property
    def status(self) -> str:
        return self._active

    @property
    def is_active(self) -> bool:
        return True if self._active == "active" else False

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "MarsRover":
        return cls(data)


class MarsPhoto(object):
    __slots__ = [
        '_id',
        '_sol',
        '_url',
        '_earth_date',
        '_total_photos',
        '_cameras',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._id = data.get("id")
        self._sol = data.get("sol")
        self._url = data.get("img_src")
        self._earth_date = data.get("earth_date")
        self._total_photos = data.get("total_photos")
        self._cameras = data.get("cameras")
        self._data = data

    @property
    def id(self) -> Union[int, None]:
        return self._id

    @property
    def sol(self) -> int:
        return self._sol

    @property
    def url(self) -> Union[str, None]:
        return self._url

    @property
    def earth_date(self) -> str:
        return self._earth_date

    @property
    def earth_datetime(self) -> datetime.datetime:
        return datetime.datetime.strptime(self._earth_date, "%Y-%m-%d")

    @property
    def total_photos(self) -> Union[int, None]:
        return self._total_photos

    @property
    def cameras(self) -> Union[List[str], None]:
        return self._cameras

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "MarsPhoto":
        return cls(data, loop=loop)


class MarsRoverResource(BaseResource):
    __slots__ = [
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(MarsRoverResource, self).__init__(data, loop=loop)
        self._data = data

    def __iter__(self):
        return self

    def __next__(self):
        for mp in self.photos:
            yield mp

    def _process_photos(self) -> Union[List[MarsPhoto], MarsPhoto, None]:
        if not (pic := self._data.get("photos")):
            return None
        elif len(pic) != 1:
            for data in pic:
                yield MarsPhoto(data)
        else:
            return MarsPhoto(pic[0])

    @property
    def photos(self) -> Union[List[MarsPhoto], MarsPhoto, None]:
        if self not in self._cache:
            self._cache[self] = self._process_photos()
        return self._cache[self]

    @property
    def all_photos(self) -> Union[List[MarsPhoto], MarsPhoto, None]:
        if (pic := f"{self}all") not in self._cache:
            self._cache[pic] = [mp for mp in self._process_photos()]
        return self._cache[pic]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "MarsRoverResource":
        return cls(data, loop=loop)


class MarsManifestResource(BaseResource):
    __slots__ = [
        '_pm',
        '_name',
        '_landing_date',
        '_launch_date',
        '_status',
        '_max_sol',
        '_max_date',
        '_total_photos',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(MarsManifestResource, self).__init__(data, loop=loop)
        self._pm = data.get("photo_manifest")
        self._name = self._pm.get("name")
        self._landing_date = self._pm.get("landing_date")
        self._launch_date = self._pm.get("launch_date")
        self._status = self._pm.get("status")
        self._max_sol = self._pm.get("max_sol")
        self._max_date = self._pm.get("max_date")
        self._total_photos = self._pm.get("total_photos")
        self._data = data

    def __iter__(self):
        return self

    def __next__(self):
        for mp in self.photos():
            yield mp

    @property
    def name(self) -> str:
        return self._name

    @property
    def landing_date(self) -> str:
        return self._landing_date

    @property
    def landing_datetime(self) -> datetime.datetime:
        return datetime.datetime.strptime(self._landing_date, "%Y-%m-%d")

    @property
    def launch_date(self) -> str:
        return self._launch_date

    @property
    def launch_datetime(self) -> datetime.datetime:
        return datetime.datetime.strptime(self._launch_date, "%Y-%m-%d")

    @property
    def status(self) -> str:
        return self._status

    @property
    def is_active(self) -> bool:
        return True if self._active == "active" else False

    @property
    def max_sol(self) -> int:
        return self._max_sol

    @property
    def max_date(self) -> str:
        return self._max_date

    @property
    def max_datetime(self) -> datetime.datetime:
        return datetime.datetime.strptime(self._max_date, "%Y-%m-%d")

    @property
    def total_photos(self) -> int:
        return self._total_photos

    def _process_photos(self) -> Union[List[MarsPhoto], MarsPhoto, None]:
        if not (mp := self._pm.get("photos")):
            return None
        elif len(mp) != 1:
            for data in mp:
                yield MarsPhoto(data)
        else:
            return MarsPhoto(mp[0])

    @property
    def photos(self) -> Union[List[MarsPhoto], MarsPhoto, None]:
        if self not in self._cache:
            self._cache[self] = self._process_photos()
        return self._cache[self]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "MarsManifestResource":
        return cls(data, loop=loop)
