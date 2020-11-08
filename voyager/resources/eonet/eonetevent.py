from typing import Any, Generator, Union

from .eonetcategory import EONETCategory
from .eonetgeometry import EONETGeometry

try:
    from .eonetsource import EONETSource
except ImportError:
    import sys
    EONETSource = sys.modules.get(f"{__package__}.EONETSource")


class EONETEvent(object):
    __slots__ = [
        '_id',
        '_title',
        '_description',
        '_link',
        '_closed',
        '_data',
    ]
    _map = {
        'categories': EONETCategory,
        'geometry': EONETGeometry,
    }
    _cache = {}

    def __init__(self, data: dict) -> None:
        self._id = data.get("id")
        self._title = data.get("title")
        self._description = data.get("description")
        self._link = data.get("link")
        self._closed = data.get("closed")
        self._data = data

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def link(self) -> str:
        return self._link

    @property
    def closed(self) -> bool:
        return self._closed

    def _process_event_meta(self, type) -> Union[Generator[Any, None, None], Any, None]:
        if not (ret := self._data.get(type)):
            return None
        from .eonetsource import EONETSource
        _class = self._map.get(type, EONETSource)
        if len(ret) != 1:
            return (_class(data) for data in ret)
        else:
            return _class(ret[0])

    @property
    def categories(self) -> Union[Generator[EONETCategory, None, None], EONETCategory, None]:
        if (cat := f"{self}categories") not in self._cache:
            self._cache[cat] = self._process_event_meta("categories")
        return self._cache[cat]

    @property
    def sources(self) -> Union[Generator[EONETSource, None, None], EONETSource, None]:
        if (src := f"{self}sources") not in self._cache:
            self._cache[src] = self._process_event_meta("source")
        return self._cache[src]

    @property
    def geometry(self) -> Union[Generator[EONETGeometry, None, None], EONETGeometry, None]:
        if (geo := f"{self}geometry") not in self._cache:
            self._cache[geo] = self._process_event_meta("geometry")
        return self._cache[geo]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "EONETEvent":
        return cls(data)
