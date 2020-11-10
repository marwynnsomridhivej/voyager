from typing import Union


_ATTRS = {
    "epic_host":       Union[str, None],
    "k2_campaign_str": Union[str, None],
    "k2_name":         Union[str, None],
    "alt_name":        Union[str, None],
    "tm_designation":  Union[str, None],
    "k2_kepmag":       Union[float, None],
    "ra_str":          Union[str, None],
    "dec_str":         Union[str, None],
    "last_update":     Union[str, None],
}


class K2Name(object):
    __slots__ = [
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "K2Name":
        return cls(data)


def _add_func(name: str):
    @property
    def fn(self) -> _ATTRS.get(name):
        return self._data.get(name)
    setattr(K2Name, name, fn)


for attr in _ATTRS:
    _add_func(attr)
