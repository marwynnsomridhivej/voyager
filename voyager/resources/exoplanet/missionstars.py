from typing import Union


_ATTRS = {
    "star_name":        Union[str, None],
    "hip_name":         Union[str, None],
    "hd_name":          Union[str, None],
    "gj_name":          Union[str, None],
    "tm_name":          Union[str, None],
    "st_exocatflag":    Union[int, None],
    "st_coronagflag":   Union[int, None],
    "st_starshadeflag": Union[int, None],
    "st_wfirstflag":    Union[int, None],
    "st_lbtiflag":      Union[int, None],
    "st_rvflag":        Union[int, None],
    "st_ppnum":         Union[int, None],
    "rastr":            Union[str, None],
    "decstr":           Union[str, None],
    "st_dist":          Union[float, None],
    "st_disterr1":      Union[float, None],
    "st_disterr2":      Union[float, None],
    "st_vmag":          Union[float, None],
    "st_vmagerr":       Union[float, None],
    "st_vmagsrc":       Union[str, None],
    "st_bmv":           Union[float, None],
    "st_bmverr":        Union[float, None],
    "st_bmvsrc":        Union[str, None],
    "st_spttype":       Union[str, None],
    "st_lbol":          Union[float, None],
    "st_lbolerr":       Union[float, None],
    "st_lbolsrc":       Union[str, None],
}


class MissionStars(object):
    __slots__ = [
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "MissionStars":
        return cls(data)


def _add_func(name: str):
    @property
    def fn(self) -> _ATTRS.get(name):
        return self._data.get(name)
    setattr(MissionStars, name, fn)


for attr in _ATTRS:
    _add_func(attr)
