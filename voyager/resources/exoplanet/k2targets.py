from typing import Union


_ATTRS = {
    "epic_number":     Union[int, None],
    "tm_name":         Union[str, None],
    "k2_campaign_str": Union[str, None],
    "k2_type":         Union[str, None],
    "rastr":           Union[str, None],
    "decstr":          Union[str, None],
    "k2_propid":       Union[float, None],
    "k2_dist":         Union[float, None],
    "k2_disterr1":     Union[float, None],
    "k2_disterr2":     Union[float, None],
    "k2_teff":         Union[float, None],
    "k2_tefferr1":     Union[float, None],
    "k2_tefferr2":     Union[float, None],
    "k2_rad":          Union[float, None],
    "k2_raderr1":      Union[float, None],
    "k2_raderr2":      Union[float, None],
    "k2_mass":         Union[float, None],
    "k2_masserr1":     Union[float, None],
    "k2_masserr2":     Union[float, None],
    "k2_kepmag":       Union[float, None],
    "k2_kepmagerr":    Union[float, None],
    "k2_kepmagflag":   Union[float, None],
    "k2_vjmag":        Union[float, None],
    "k2_vjmagerr":     Union[float, None],
    "k2_kmag":         Union[float, None],
    "k2_kmagerr":      Union[float, None],
}


class K2Target(object):
    __slots__ = [
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "K2Target":
        return cls(data)


def _add_func(name: str):
    @property
    def fn(self) -> _ATTRS.get(name):
        return self._data.get(name)
    setattr(K2Target, name, fn)


for attr in _ATTRS:
    _add_func(attr)
