import datetime
from asyncio.events import AbstractEventLoop
from typing import Any, Generator, Union

from .base import BaseResource
from .sentry import (SentryBase, SentryDataO, SentryDataR, SentryDataS,
                     SentryDataV, SentrySummary)

__all__ = [
    'SentryResource',
]


_MAP = {
    'os': SentrySummary,
    'od': SentryDataO,
    'sd': SentryDataS,
    'vd': SentryDataV,
    'rd': SentryDataR,
}


def _handle(pot_int: str, default: Any = None) -> Union[Any, None]:
    try:
        if default:
            return default(pot_int)
        return int(pot_int)
    except Exception:
        return pot_int


class SentryResource(BaseResource):
    __slots__ = [
        '_count',
        '_removed',
        '_error',
        '_mode',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(SentryResource, self).__init__(data, loop=loop)
        self._count = _handle(data.get("count"))
        self._removed = data.get(
            "removed",
            lambda s: datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        )
        self._error = data.get("error")
        self._mode = data.get("mode")
        self._data = data

    def __len__(self) -> int:
        if self._count is None:
            self._count = len(self._data.get("data"))
        return self._count

    def __iter__(self):
        return self

    def __next__(self):
        for dt in self.data:
            yield dt

    @property
    def count(self) -> Union[int, None]:
        return self._count

    @property
    def summary(self) -> Union[SentrySummary, None]:
        if (sm := f"{self}summary") not in self._cache:
            if (smr := self._data.get("summary")):
                self._cache[sm] = SentrySummary(smr)
            else:
                self._cache[sm] = None
        return self._cache[sm]

    def _process_data(self) -> Union[Generator[SentryBase, None, None], SentryBase, None]:
        if not (dt := self._data.get("data")):
            return None
        _class = _MAP.get(f"{self._mode}d")
        if len(dt) != 1:
            return (_class(data) for data in dt)
        else:
            return _class(dt[0])

    @property
    def data(self) -> Union[Generator[SentryBase, None, None], SentryBase, None]:
        if (dt := f"{self}data") not in self._cache:
            self._cache[dt] = self._process_data()
        return self._cache[dt]

    @property
    def removed(self) -> Union[datetime.datetime, str, None]:
        return self._removed

    @property
    def error(self) -> Union[str, None]:
        return self._error

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "SentryResource":
        return cls(data, loop=loop)
