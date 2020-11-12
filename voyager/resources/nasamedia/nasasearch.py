from typing import Generator, Union
from .nasamedia import NASAMediaAsset
from .nasamedialink import NASAMediaLink


class NASAMediaCollection(object):
    __slots__ = [
        '_version',
        '_metadata',
        '_href',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict) -> None:
        self._version = data.get("version")
        self._metadata = data.get("metadata")
        self._href = data.get("href")
        self._data = data

    @property
    def version(self) -> str:
        return self._version

    @property
    def total_hits(self) -> int:
        return self._metadata.get("total_hits", 0)

    @property
    def href(self) -> str:
        return self._href

    @property
    def url(self) -> str:
        return self.href

    def _process_items(self) -> Union[Generator[NASAMediaAsset, None, None], NASAMediaAsset, None]:
        if not (ma := self._data.get("items")):
            return None
        elif len(ma) != 1:
            return (NASAMediaAsset(item) for item in ma)
        else:
            return NASAMediaAsset(ma[0])

    @property
    def items(self) -> Union[Generator[NASAMediaAsset, None, None], NASAMediaAsset, None]:
        if (ma := f"{self}asset") not in self._cache:
            self._cache[ma] = self._process_items()
        return self._cache[ma]

    def _process_links(self) -> Union[Generator[NASAMediaLink, None, None], NASAMediaLink, None]:
        if not (lk := self._data.get("links")):
            return None
        elif len(lk) != 1:
            return (NASAMediaLink(data) for data in lk)
        else:
            return NASAMediaLink(lk[0])

    @property
    def links(self) -> Union[Generator[NASAMediaLink, None, None], NASAMediaLink, None]:
        if (lk := f"{self}links") not in self._cache:
            self._cache[lk] = self._process_links()
        return self._cache[lk]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "NASAMediaCollection":
        return cls(data)
