import datetime
from asyncio.events import AbstractEventLoop
from io import BytesIO
from typing import Tuple, Union

from .base import BaseResource
from ..decorators import check_pil_importable

try:
    from PIL import Image
except ImportError:
    pass

__all__ = [
    'APODResource',
]


class APODResource(BaseResource):
    __slots__ = [
        '_msg',
        '_service_version',
        '_concepts',
        '_date',
        '_explanation',
        '_url',
        '_media_type',
        '_title',
        '_bytes',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(APODResource, self).__init__(data, loop=loop)
        self._msg = data.get("msg")
        self._service_version = data.get("service_version", "v1")
        self._concepts = data.get("concepts")
        self._copyright = data.get("copyright", "Public Domain")
        self._date = data.get("date")
        self._explanation = data.get("explanation")
        self._url = data.get("hdurl") or data.get("url")
        self._media_type = data.get("media_type")
        self._title = data.get("title")
        self._bytes = data.get("raw")
        if not self._msg:
            del self.error
        self._data = data

    @property
    def msg(self) -> Union[str, None]:
        return self._msg

    @property
    def service_version(self) -> str:
        return self._service_version

    @property
    def concepts(self) -> Union[str, None]:
        return self._concepts

    @property
    def copyright(self) -> str:
        return self._copyright

    @property
    def date(self) -> str:
        return self._date

    @property
    def explanation(self) -> Union[str, None]:
        return self._explanation

    @property
    def url(self) -> Union[str, None]:
        return self._url

    @property
    def media_type(self) -> Union[str, None]:
        return self._media_type

    @property
    def title(self) -> Union[str, None]:
        return self._title

    def _process_datetime(self) -> datetime.datetime:
        if not isinstance(self._date, datetime.datetime):
            return datetime.datetime.strptime(self._date)
        return self._date

    @property
    def datetime(self) -> datetime.datetime:
        if self not in self._cache:
            self._cache[self] = self._process_datetime()
        return self._cache[self]

    @property
    def error(self) -> Tuple[int, str, str]:
        return self._code, self.msg, self._service_version

    @property
    def bytesio(self) -> BytesIO:
        return BytesIO(self._bytes)

    @property
    def bytes(self) -> bytes:
        return self._bytes

    @property
    @check_pil_importable
    def image(self) -> Image:
        return Image.open(self.bytesio)

    @check_pil_importable
    async def show(self) -> None:
        return await self.loop.run_in_executor(None, self.image.show)

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "APODResource":
        return cls(data, loop=loop)
