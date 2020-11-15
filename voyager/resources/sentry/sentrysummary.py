from typing import Union
from . import _handle


_ATTRS = {
    "energy": Union[float, str],
    "method": str,
    "darc": str,
    "ip": Union[float, str],
    "h": Union[float, str],
    "nobs": Union[int, str],
    "mass": Union[float, str],
    "v_inf": Union[float, str],
    "first_obs": str,
    "ndop": Union[int, str],
    "pdate": str,
    "cdate": str,
    "ps_cum": Union[float, str],
    "diameter": Union[float, str],
    "v_imp": Union[float, str],
    "ndel": Union[int, str],
    "ps_max": Union[float, str],
    "last_obs": str,
    "fullname": str,
    "ts_max": Union[int, str],
    "n_imp": Union[int, str],
    "nsat": Union[int, str],
    "des": str,
}


class SentrySummary(object):
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
    def from_dict(cls, data: dict) -> "SentrySummary":
        return cls(data)


def _add_func(name: str):
    @property
    def fn(self) -> _ATTRS.get(name):
        if name not in self._cache:
            self._cache[name] = _handle(self._data.get(name))
        return self._cache[name]
    setattr(SentrySummary, name, fn)


for attr in _ATTRS:
    _add_func(attr)
