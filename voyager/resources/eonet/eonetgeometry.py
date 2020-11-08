import datetime
from typing import Any, Generator, List, Union

from .eonetcategory import EONETCategory

try:
    from .eonetsource import EONETSource
except ImportError:
    import sys
    EONETSource = sys.modules.get(f"{__package__}.EONETSource")


class EONETGeometry(object):
    __slots__ = [
        '_id',
        '_title',
        '_description',
        '_link',
        '_closed',
        '_mag_val',
        '_mag_unit',
        '_date',
        '_type',
        '_coords',
        '_data'
    ]
    _map = {
        "categories": EONETCategory,
    }
    _cache = {}

    def __init__(self, data: dict) -> None:
        _prop = data.get("properties", data)
        self._id = _prop.get("id")
        self._title = _prop.get("title")
        self._description = _prop.get("description")
        self._link = _prop.get("link")
        self._closed = _prop.get("closed")
        self._date = _prop.get("date")
        self._mag_val = _prop.get("magnitudeValue")
        self._mag_unit = _prop.get("magnitudeUnit")

        if (geo := data.get("geometry")):
            self._coords = geo.get("coordinates")
            self._type = geo.get("type")
        else:
            self._coords = data.get("coordinates")
            self._type = data.get("type")
        self._data = data

    @property
    def magnitude_value(self) -> Union[Any, None]:
        return self._mag_val

    @property
    def mag_val(self) -> Union[Any, None]:
        return self.magnitude_value

    @property
    def date(self) -> str:
        return self._date

    @property
    def datetime(self) -> datetime.datetime:  # TODO: Implement this
        pass

    @property
    def coordinates(self) -> Union[List[List[float]], List[float], None]:
        return self._coords

    def _process_meta(self, type: str) -> Union[Generator[Any, None, None], Any, None]:
        if not (meta := self._data.get(type)):
            return None
        from .eonetsource import EONETSource
        _class = self._map.get(type, EONETSource)
        if len(meta) != 1:
            return (_class(data) for data in meta)
        else:
            return _class(meta[0])

    @property
    def categories(self) -> Union[Generator[EONETCategory, None, None], EONETCategory, None]:
        if (cat := f"{self}categories") not in self._cache:
            self._cache[cat] = self._process_meta("categories")
        return self._cache[cat]

    @property
    def sources(self) -> Union[Generator[EONETSource, None, None], EONETSource, None]:
        if (src := f"{self}sources") not in self._cache:
            self._cache[src] = self._process_meta("sources")
        return self._cache[src]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "EONETGeometry":
        return cls(data)
