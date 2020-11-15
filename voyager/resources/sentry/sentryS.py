from typing import Union

from . import _handle
from .sentrybase import SentryBase


_ATTRS = {
    "des": Union[int, str],
    "fullname": str,
    "range": str,
    "n_imp": Union[int, str],
    "ip": Union[float, str],
    "v_inf": Union[float, str],
    "last_obs": str,
    "last_obs_jd": Union[float, str],
    "h": Union[float, str],
    "diameter": Union[float, str],
    "ps_cum": Union[float, str],
    "ps_max": Union[float, str],
    "ts_max": Union[int, str],
}


class SentryDataS(SentryBase):
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
    def from_dict(cls, data: dict) -> "SentryDataS":
        return cls(data)


def _add_func(name: str):
    @property
    def fn(self) -> _ATTRS.get(name):
        if name not in self._cache:
            self._cache[name] = _handle(self._data.get(name))
        return self._cache[name]
    setattr(SentryDataS, name, fn)


for attr in _ATTRS:
    _add_func(attr)
