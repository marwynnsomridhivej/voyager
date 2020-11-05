import datetime
from asyncio.events import AbstractEventLoop
from io import BytesIO
from typing import Tuple, Union

from ..decorators import check_pil_importable
from .base import BaseResource

try:
    from PIL import Image
except ImportError:
    pass


__all__ = [
    'EarthImageryResource',
    'EarthAssetResource',
]


class EarthResource(object):
    __slots__ = [
        '_dataset',
        '_planet',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._dataset = data.get("dataset")
        self._planet = data.get("earth")
        self._data = data

    @property
    def dataset(self) -> str:
        return self._dataset

    @property
    def planet(self) -> str:
        return self._planet

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "EarthResource":
        return cls(data)


class EarthAssetResource(BaseResource):
    __slots__ = [
        '_date',
        '_id',
        '_service_version',
        '_url',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(EarthAssetResource, self).__init__(data, loop=loop)
        self._date = data.get("date")
        self._id = data.get("id")
        self._service_version = data.get("service_version")
        self._url = data.get("url")

    @property
    def date(self) -> str:  # TODO: Implement datetime.datetime
        return self._date

    @property
    def id(self) -> str:
        return self._id

    def _process_resource(self) -> Union[EarthResource, None]:
        if not (res := self._data.get("resource")):
            return None
        else:
            return EarthResource(res)

    @property
    def resource(self) -> Union[EarthResource, None]:
        if self not in self._cache:
            self._cache[self] = self._process_resource()
        return self._cache[self]

    @property
    def service_version(self) -> str:
        return self._service_version

    @property
    def url(self) -> str:
        return self._url

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "EarthAssetResource":
        return cls(data, loop=loop)


class EarthImageryResource(BaseResource):
    __slots__ = [
        '_latitude',
        '_longitude',
        '_dimensions',
        '_date',
        '_cloud_score',
        '_raw',
        '_data',
    ]

    def __init__(self, data: dict, raw: bytes = None,
                 loop: AbstractEventLoop = None) -> None:
        super(EarthImageryResource, self).__init__(data, loop=loop)
        self._latitude = data.get("lat")
        self._longitude = data.get("lon")
        self._dimensions = data.get("dim")
        self._date = data.get("date")
        self._cloud_score = data.get("cloud_score")
        self._raw = raw
        self._data = data

    @property
    def latitude(self) -> float:
        return self._latitude

    @property
    def longitude(self) -> float:
        return self._longitude

    @property
    def dimensions(self) -> Tuple[float]:
        return self._dimensions, self._dimensions

    @property
    def date(self) -> str:
        return self._date

    @property
    def datetime(self) -> datetime.datetime:
        return datetime.datetime.strptime(self._date, "%Y-%m-%d")

    @property
    def cloud_score(self) -> bool:  # Not currently available
        return self._cloud_score

    @property
    def raw(self) -> bytes:
        return self._bytes

    @property
    @check_pil_importable
    def image(self) -> Image:
        return Image.open(BytesIO(self._bytes))

    @check_pil_importable
    async def show(self) -> None:
        return await self.loop.run_in_executor(None, self.image.show)

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict, raw: bytes = None,
                  loop: AbstractEventLoop = None) -> "EarthImageryResource":
        return cls(data, raw=raw, loop=loop)
