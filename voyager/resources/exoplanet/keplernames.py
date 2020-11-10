from typing import Union


_ATTRS = {
    "kepid":          Union[int, None],
    "ra":             Union[float, None],
    "ra_err":         Union[float, None],
    "dec":            Union[float, None],
    "dec_err":        Union[float, None],
    "ra_str":         Union[str, None],
    "dec_str":        Union[str, None],
    "kepoi_name":     Union[str, None],
    "kepler_name":    Union[str, None],
    "alt_name":       Union[str, None],
    "tm_designation": Union[str, None],
    "koi_list_flag":  Union[str, None],
    "last_update":    Union[str, None],
}


class KeplerNames(object):
    __slots__ = [
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "KeplerNames":
        return cls(data)


def _add_func(name: str):
    @property
    def fn(self) -> _ATTRS.get(name):
        return self._data.get(name)
    setattr(KeplerNames, name, fn)


for attr in _ATTRS:
    _add_func(attr)
