from asyncio.events import AbstractEventLoop
from typing import Generator, List, Union

from .base import BaseResource
from .genelab import GenelabStudy, GenelabHit


__all__ = [
    'GenelabResource',
    'GenelabDatasetResource',
    'GenelabMetadataResource',
]


class GenelabResource(BaseResource):
    __slots__ = [
        '_hits',
        '_input',
        '_page_number',
        '_total_hits',
        '_page_total',
        '_success',
        '_page_size',
        '_data'
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(GenelabResource, self).__init__(data, loop=loop)
        self._hits = data.get("hits")
        self._input = data.get("input")
        self._page_number = data.get("page_number")
        self._total_hits = data.get("total_hits")
        self._page_total = data.get("page_total")
        self._success = data.get("success")
        self._page_size = data.get("page_size")
        self._data = data

    def __iter__(self):
        return self

    def __next__(self):
        for sd in self.studies:
            yield sd

    @property
    def hits(self) -> int:
        return self._hits

    @property
    def input(self) -> str:
        return self._input

    @property
    def page_number(self) -> int:
        return self._page_number

    @property
    def total_hits(self) -> int:
        return self._total_hits

    @property
    def page_total(self) -> int:
        return self._page_total

    @property
    def total_pages(self) -> int:
        return self.page_total

    @property
    def success(self) -> bool:
        return self._success

    @property
    def valid_input(self) -> Union[List[int], None]:
        if (vi := f"{self}input") not in self._cache:
            self._cache[vi] = self._data.get("valid_input")
        return self._cache[vi]

    def _process_studies(self) -> Union[Generator[GenelabStudy, None, None], GenelabStudy, None]:
        if not (sd := self._data.get("studies")):
            return None
        elif len(sd) != 1:
            return (GenelabStudy(name, data) for name, data in sd.items())
        else:
            nd = [(name, data) for name, data in sd.items()]
            return GenelabStudy(nd[0][0], nd[0][1])

    @property
    def studies(self) -> Union[Generator[GenelabStudy, None, None], GenelabStudy, None]:
        if (sd := f"{self}study") not in self._cache:
            self._cache[sd] = self._process_studies()
        return self._cache[sd]

    @property
    def page_size(self) -> int:
        return self._page_size

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "GenelabResource":
        return cls(data, loop=loop)


class GenelabDatasetResource(BaseResource):
    __slots__ = [
        '_took',
        '_timed_out',
        '_hits',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(GenelabDatasetResource, self).__init__(data, loop=loop)
        self._took = data.get("took")
        self._timed_out = data.get("timed_out")
        self._hits = data.get("hits")
        self._data = data

    @property
    def took(self) -> int:
        return self._took

    @property
    def timed_out(self) -> bool:
        return self._timed_out

    @property
    def total_hits(self) -> Union[int, None]:
        return self._hits.get("total_hits") if self._hits else None

    @property
    def max_score(self) -> Union[float, None]:
        return self._hits.get("max_score") if self._hits else None

    def _process_hits(self) -> Union[Generator[GenelabHit, None, None], GenelabHit, None]:
        if not self._hits or not (ht := self._hits.get("hits")):
            return None
        elif len(ht) != 1:
            return (GenelabHit(data) for data in ht)
        else:
            return GenelabHit(ht[0])

    @property
    def hits(self) -> Union[Generator[GenelabHit, None, None], GenelabHit, None]:
        if self not in self._cache:
            self._cache = self._process_hits()
        return self._cache[self]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "GenelabDatasetResource":
        return cls(data, loop=loop)


class GenelabMetadataResource(BaseResource):
    __slots__ = [
        '_hits',
        '_input',
        '_success',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(GenelabMetadataResource, self).__init__(data, loop=loop)
        self._hits = data.get("hits")
        self._input = data.get("input")
        self._success = data.get("success")
        self._data = data

    @property
    def hits(self) -> int:
        return self._hits

    @property
    def input(self) -> str:
        return self._input

    @property
    def success(self) -> bool:
        return self._success

    @property
    def study(self) -> dict:
        return self._data.get("study")

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "GenelabMetadataResource":
        return cls(data, loop=loop)
