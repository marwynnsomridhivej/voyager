from typing import Union


_ATTRS = {
    "epic_name":       Union[str, None],
    "epic_candname":   Union[str, None],
    "pl_name":         Union[str, None],
    "k2c_refdisp":     Union[str, None],
    "k2c_reflink":     Union[str, None],
    "k2c_disp":        Union[str, None],
    "k2c_note":        Union[str, None],
    "k2_campaign_str": Union[int, None],
    "k2c_recentflag":  Union[int, None],
    "pl_orbper":       Union[float, None],
    "pl_orbpererr1":   Union[float, None],
    "pl_orbpererr2":   Union[float, None],
    "pl_orbperlim":    Union[int, None],
    "pl_tranmid":      Union[float, None],
    "pl_tranmiderr1":  Union[float, None],
    "pl_tranmiderr2":  Union[float, None],
    "pl_tranmidlim":   Union[int, None],
    "pl_ratdor":       Union[float, None],
    "pl_ratdorerr1":   Union[float, None],
    "pl_ratdorerr2":   Union[float, None],
    "pl_ratdorlim":    Union[float, None],
    "pl_ratror":       Union[float, None],
    "pl_ratrorerr1":   Union[float, None],
    "pl_ratrorerr2":   Union[float, None],
    "pl_ratrorlim":    Union[int, None],
    "pl_rade":         Union[float, None],
    "pl_radeerr1":     Union[float, None],
    "pl_radeerr2":     Union[float, None],
    "pl_radelim":      Union[int, None],
    "st_rad":          Union[float, None],
    "st_raderr1":      Union[float, None],
    "st_raderr2":      Union[float, None],
    "st_radlim":       Union[int, None],
    "st_kep":          Union[float, None],
    "st_keperr":       Union[float, None],
    "st_keplim":       Union[int, None],
    "st_k2":           Union[float, None],
    "st_k2err":        Union[float, None],
    "st_k2lim":        Union[int, None],
}


class K2Candidate(object):
    __slots__ = [
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "K2Candidate":
        return cls(data)


def _add_func(name: str):
    @property
    def fn(self) -> _ATTRS.get(name):
        return self._data.get(name)
    setattr(K2Candidate, name, fn)


for attr in _ATTRS:
    _add_func(attr)
