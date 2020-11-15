from typing import Union

from . import _handle
from .sentrybase import SentryBase


_ATTRS = {
    "width": Union[float, str],
    "energy": Union[float, str],
    "ts": Union[int, str],
    "ip": Union[float, str],
    "stretch": Union[float, str],
    "date": str,
    "dist": Union[float, str],
    "sigma_lov": Union[float, str],
    "sigma_imp": Union[float, str],
    "fullname": str,
    "id": str,
    "ps": Union[float, str],
    "des": str,
}


class SentryDataV(SentryBase):
    __slots__ = [
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "SentryDataV":
        return cls(data)


def _add_func(name: str):
    @property
    def fn(self) -> _ATTRS.get(name):
        if name not in self._cache:
            self._cache[name] = _handle(self._data.get(name))
        return self._cache[name]
    setattr(SentryDataV, name, fn)


for attr in _ATTRS:
    _add_func(attr)
