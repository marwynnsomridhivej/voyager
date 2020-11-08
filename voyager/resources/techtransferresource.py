import re
from asyncio.events import AbstractEventLoop
from typing import Any, Generator, List, Union

from .base import BaseResource

_TAG_RX = re.compile(r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
_agency = {
    'AFRC': 'Armstrong Flight Research Center',
    'ARC': 'Ames Research Center',
    'DFRC': 'Dryden Flight Research Center',
    'GRC': 'Glenn Research Center',
    'GSFC': 'Goddard Space Flight Center',
    'JPL': 'Jet Propulsion Laboratory',
    'JSC': 'Johnson Space Center',
    'KSC': 'Kennedy Space Center',
    'LARC': 'Langley Research Center',
    'MSFC': 'Marshall Space Flight Center',
    'SSC': 'Stennis Space Center',
}


__all__ = [
    'TechTransferResource',
]


def _extract(data: List[str], index: int, default: Any = None) -> Union[Any, None]:
    try:
        return data[index]
    except KeyError:
        return default


class TechTransferPatent(object):
    __slots__ = [
        '_id',
        '_reference_number',
        '_title',
        '_description',
        '_category',
        '_agency',
        '_image_url',
        '_relevance',
        '_data',
    ]
    _ATTRS = [
        'id',
        'reference_number',
        'title',
        'description',
        'category',
        'agency',
        'image_url',
        'relevance',
    ]
    _cache = {}

    def __init__(self, data: List[str]) -> None:
        self._id = _extract(data, 0)
        self._reference_number = _extract(data, 1)
        self._title = re.sub(_TAG_RX, "", _extract(data, 2, default=""))
        self._description = re.sub(_TAG_RX, "", _extract(data, 3, default=""))
        self._category = _extract(data, 5)
        self._agency = _agency.get(_extract(data, 9))
        self._image_url = _extract(data, 10, default="").replace("\\", "")
        self._relevance = _extract(data, 12)
        self._data = data

    @property
    def id(self) -> str:
        return self._id

    @property
    def reference_number(self) -> str:
        return self._reference_number

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def category(self) -> str:
        return self._category

    @property
    def agency(self) -> str:
        return self._agency

    @property
    def image_url(self) -> Union[str, None]:
        return self._image_url

    @property
    def relevance(self) -> Union[float, None]:
        return self._relevance

    @property
    def to_dict(self) -> dict:
        if self not in self._cache:
            self._cache[self] = {attr: getattr(self, attr) for attr in self._ATTRS}
        return self._cache[self]

    @classmethod
    def from_dict(cls, data: dict) -> "TechTransferPatent":
        return cls([
            data.get("id"),
            data.get("reference_number"),
            data.get("title"),
            data.get("description"),
            data.get("reference_number"),
            data.get("category"),
            "",
            "",
            "",
            data.get("agency"),
            data.get("image_url"),
            "",
            data.get("relevance"),
        ])


class TechTransferPatentIssued(TechTransferPatent):
    def __init__(self, data: List[str]) -> None:
        super(TechTransferPatentIssued, self).__init__(data)


class TechTransferSoftware(object):
    __slots__ = [
        '_id',
        '_reference_number',
        '_title',
        '_description',
        '_category',
        '_release_type',
        '_note',
        '_source_code',
        '_agency',
        '_relevance',
        '_data',
    ]
    _ATTRS = [
        'id',
        'reference_number',
        'title',
        'description',
        'category',
        'release_type',
        'note',
        'source_code',
        'agency',
        'relevance',
    ]
    _cache = {}

    def __init__(self, data: List[str]) -> None:
        self._id = _extract(data, 0)
        self._reference_number = _extract(data, 1)
        self._title = re.sub(_TAG_RX, "", _extract(data, 2, default=""))
        self._description = re.sub(_TAG_RX, "", _extract(data, 3, default=""))
        self._category = _extract(data, 5)
        self._release_type = _extract(data, 6)
        self._note = re.sub(_TAG_RX, "", _extract(data, 7, default="")).replace("\\", "")
        self._source_code = re.sub(_TAG_RX, "", _extract(data, 8, default="")).replace("\\", "")
        self._agency = _agency.get(_extract(data, 9))
        self._relevance = _extract(data, 12)
        self._data = data

    @property
    def id(self) -> str:
        return self._id

    @property
    def reference_number(self) -> str:
        return self._reference_number

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def category(self) -> str:
        return self._category

    @property
    def release_type(self) -> str:
        return self._release_type

    @property
    def note(self) -> Union[str, None]:
        return self._note

    @property
    def source_code(self) -> Union[str, None]:
        return self._source_code

    @property
    def agency(self) -> str:
        return self._agency

    @property
    def relevance(self) -> Union[float, None]:
        return self._relevance

    @property
    def to_dict(self) -> dict:
        if self not in self._cache:
            self._cache[self] = {attr: getattr(self, f"_{attr}") for attr in self._ATTRS}
        return self._cache[self]

    @classmethod
    def from_dict(cls, data: dict) -> "TechTransferSoftware":
        return cls([
            data.get("id"),
            data.get("reference_number"),
            data.get("title"),
            data.get("description"),
            data.get("reference_number"),
            data.get("category"),
            data.get("release_type"),
            data.get("note"),
            data.get("source_code"),
            data.get("agency"),
            "",
            "",
            data.get("relevance"),
        ])


class TechTransferSpinoff(object):
    __slots__ = [
        '_id',
        '_reference_number',
        '_title',
        '_description',
        '_category',
        '_agency',
        '_relevance',
        '_data',
    ]
    _ATTRS = [
        'id',
        'reference_number',
        'title',
        'description',
        'category',
        'agency',
        'relevance',
    ]
    _cache = {}

    def __init__(self, data: List[str]) -> None:
        self._id = _extract(data, 0)
        self._reference_number = _extract(data, 1)
        self._title = re.sub(_TAG_RX, "", _extract(data, 2, default=""))
        self._description = re.sub(_TAG_RX, "", _extract(data, 3, default=""))
        self._category = _extract(data, 5)
        self._agency = _agency.get(_extract(data, 9))
        self._relevance = _extract(data, 12)
        self._data = data

    @property
    def id(self) -> str:
        return self._id

    @property
    def reference_number(self) -> str:
        return self._reference_number

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def category(self) -> str:
        return self._category

    @property
    def agency(self) -> str:
        return self._agency

    @property
    def relevance(self) -> Union[float, None]:
        return self._relevance

    @property
    def to_dict(self) -> dict:
        if self not in self._cache:
            self._cache[self] = {attr: getattr(self, attr) for attr in self._ATTRS}
        return self._cache[self]

    @classmethod
    def from_dict(cls, data: dict) -> "TechTransferSpinoff":
        return cls([
            data.get("id"),
            data.get("reference_number"),
            data.get("title"),
            data.get("description"),
            data.get("reference_number"),
            data.get("category"),
            "",
            "",
            "",
            data.get("agency"),
            "",
            "",
            data.get("relevance"),
        ])


class TechTransferResource(BaseResource):
    __slots__ = [
        '_type',
        '_count',
        '_total',
        '_per_page',
        '_page',
        '_data',
    ]
    _mapping = {
        'patent': TechTransferPatent,
        'patent_issued': TechTransferPatentIssued,
        'software': TechTransferSoftware,
        'spinoff': TechTransferSpinoff,
    }
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(TechTransferResource, self).__init__(data, loop=loop)
        self._type = data.get("type")
        self._count = data.get("count")
        self._total = data.get("total")
        self._per_page = data.get("perpage")
        self._page = data.get("page")

    def __len__(self) -> int:
        return self._count

    def _process_results(self) -> Union[Generator[Any, None, None], Any, None]:
        if not (rs := self._data.get("results")):
            return None
        elif len(rs) != 1:
            for data in rs:
                yield self._mapping.get(self._type)(data)
        else:
            return self._mapping.get(self._type)(rs[0])

    @property
    def results(self) -> Union[Generator[Any, None, None], Any, None]:
        if self not in self._cache:
            self._cache[self] = self._process_results()
        return self._cache[self]

    @property
    def count(self) -> int:
        return self._count

    @property
    def total(self) -> int:
        return self._total

    @property
    def per_page(self) -> int:
        return self._per_page

    @property
    def page(self) -> int:
        return self._page

    @property
    def current_page(self) -> int:
        return self.page

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "TechTransferResource":
        return cls(data, loop=loop)
