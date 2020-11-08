from asyncio.events import AbstractEventLoop
from typing import Any, Generator, Union

from .base import BaseResource
from .eonet import EONETCategory, EONETEvent, EONETGeometry, EONETSource

__all__ = [
    'EONETCategoryResource',
    'EONETEventResource',
    'EONETGeoJSONEventResource',
    'EONETLayerResource',
    'EONETSourceResource',
]


class EONETCategoryResource(BaseResource):
    __slots__ = [
        '_title',
        '_description',
        '_link',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(EONETCategoryResource, self).__init__(data, loop=loop)
        self._title = data.get("title")
        self._description = data.get("description")
        self._link = data.get("link")
        self._data = data

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
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "EONETCategoryResource":
        return cls(data, loop=loop)


class EONETEventResource(BaseResource):
    __slots__ = [
        '_title',
        '_description',
        '_link',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(EONETEventResource, self).__init__(data, loop=loop)
        self._title = data.get("title")
        self._description = data.get("description")
        self._link = data.get("link")
        self._data = data

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def link(self) -> str:
        return self._link

    def _process_events(self) -> Union[Generator[EONETEvent, None, None], EONETEvent, None]:
        if not (ev := self._data.get("events")):
            return None
        elif len(ev) != 1:
            return (EONETEvent(data) for data in ev)
        else:
            return EONETEvent(ev[0])

    @property
    def events(self) -> Union[Generator[EONETEvent, None, None], EONETEvent, None]:
        if self not in self._cache:
            self._cache[self] = self._process_events()
        return self._cahce[self]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "EONETEventResource":
        return cls(data, loop=loop)


class EONETGeoJSONEventResource(EONETEventResource):
    __slots__ = [
        '_type',
        '_id',
        '_title',
        '_description',
        '_link',
        '_closed',
        '_data',
    ]
    _map = {
        "categories": EONETCategory,
        "sources": EONETSource,
        "features": EONETGeometry,
    }
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(EONETGeoJSONEventResource, self).__init__(data, loop=loop)
        self._type = data.get("type")
        self._id = data.get("id")
        self._title = data.get("title")
        self._description = data.get("description")
        self._link = data.get("link")
        self._closed = data.get("closed")
        self._data = data

    @property
    def type(self) -> str:
        return self._type

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
    def closed(self) -> Union[bool, None]:
        return self._closeds

    def _process_meta(self, type: str) -> Union[Generator[Any, None, None], Any, None]:
        if not (meta := self._data.get(type)):
            return None
        _class = self._map.get(type)
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
    def features(self) -> Union[Generator[EONETGeometry, None, None], EONETGeometry, None]:
        if (geo := f"{self}features") not in self._cache:
            self._cache[geo] = self._process_meta("features")
        return self._cache[geo]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "EONETGeoJSONEventResource":
        return cls(data, loop=loop)


class EONETLayerResource(BaseResource):
    __slots__ = [
        '_title',
        '_description',
        '_link',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(EONETLayerResource, self).__init__(data, loop=loop)
        self._title = data.get("title")
        self._description = data.get("description")
        self._link = data.get("link")
        self._data = data

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
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "EONETLayerResource":
        return cls(data, loop=loop)


class EONETSourceResource(BaseResource):
    __slots__ = [
        '_title',
        '_description',
        '_link',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(EONETSourceResource, self).__init__(data, loop=loop)
        self._title = data.get("title")
        self._description = data.get("description")
        self._link = data.get("link")
        self._data = data

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def link(self) -> str:
        return self._link

    def _process_sources(self) -> Union[Generator[EONETSource, None, None], EONETSource, None]:
        if not (sc := self._data.get("sources")):
            return None
        elif len(sc) != 1:
            return (EONETSource(data, self._loop) for data in sc)
        else:
            return EONETSource(sc[0], self._loop)

    @property
    def sources(self) -> Union[Generator[EONETSource, None, None], EONETSource, None]:
        if self not in self._cache:
            self._cache[self] = self._process_sources()
        return self._cache[self]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "EONETSourceResource":
        return cls(data, loop=loop)
