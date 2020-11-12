from typing import Generator, List, Union
from .nasamedialink import NASAMediaLink


class NASAMediaData(object):
    __slots__ = [
        '_nasa_id',
        '_description',
        '_title',
        '_keywords',
        '_center',
        '_date_created',
        '_media_type',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._nasa_id = data.get("nasa_id")
        self._description = data.get("description")
        self._title = data.get("title")
        self._keywords = data.get("keywords")
        self._center = data.get("center")
        self._date_created = data.get("date_created")
        self._media_type = data.get("media_type")
        self._data = data

    @property
    def nasa_id(self) -> str:
        return self._nasa_id

    @property
    def id(self) -> str:
        return self.nasa_id

    @property
    def description(self) -> str:
        return self._description

    @property
    def title(self) -> str:
        return self._title

    @property
    def keywords(self) -> List[str]:
        return self._keywords

    @property
    def center(self) -> str:
        return self._center

    @property
    def date_created(self) -> str:
        return self._date_created

    @property
    def media_type(self) -> str:
        return self._media_type

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "NASAMediaData":
        return cls(data)


class NASAMediaAsset(object):
    __slots__ = [
        '_href',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict) -> None:
        self._href = data.get("href")
        self._data = data

    def _process_data(self) -> Union[Generator[NASAMediaData, None, None], NASAMediaData, None]:
        if not (dt := self._data.get("data")):
            return None
        elif len(dt) != 1:
            return (NASAMediaData(data) for data in dt)
        else:
            return NASAMediaData(dt[0])

    @property
    def data(self) -> Union[Generator[NASAMediaData, None, None], NASAMediaData, None]:
        if self not in self._cache:
            self._cache[self] = self._process_data()
        return self._cache[self]

    @property
    def href(self) -> str:
        return self._href

    @property
    def url(self) -> str:
        return self.href

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "NASAMediaAsset":
        return cls(data)
