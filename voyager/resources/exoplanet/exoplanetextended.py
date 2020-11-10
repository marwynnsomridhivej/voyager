from typing import Union


_ATTRS = {
    "mpl_hostname":     Union[str, None],
    "mpl_letter":       Union[str, None],
    "mpl_def":          Union[int, None],
    "mpl_reflink":      Union[str, None],
    "mpl_discmethod":   Union[str, None],
    "mpl_pnum":         Union[int, None],
    "mpl_orbper":       Union[float, None],
    "mpl_orbpererr1":   Union[float, None],
    "mpl_orbpererr2":   Union[float, None],
    "mpl_orbperlim":    Union[int, None],
    "mpl_orbsmax":      Union[float, None],
    "mpl_orbsmaxerr1":  Union[float, None],
    "mpl_orbsmaxerr2":  Union[float, None],
    "mpl_orbsmaxlim":   Union[int, None],
    "mpl_orbeccen":     Union[float, None],
    "mpl_orbeccenerr1": Union[float, None],
    "mpl_orbeccenerr2": Union[float, None],
    "mpl_orbeccenlim":  Union[int, None],
    "mpl_orbincl":      Union[float, None],
    "mpl_orbinclerr1":  Union[float, None],
    "mpl_orbinclerr2":  Union[float, None],
    "mpl_orbincllim":   Union[int, None],
    "mpl_bmassj":       Union[float, None],
    "mpl_bmassjerr1":   Union[float, None],
    "mpl_bmassjerr2":   Union[float, None],
    "mpl_bmassjlim":    Union[int, None],
    "mpl_bmassprov":    Union[float, None],
    "mpl_radj":         Union[float, None],
    "mpl_radjerr1":     Union[float, None],
    "mpl_radjerr2":     Union[float, None],
    "mpl_radjlim":      Union[int, None],
    "mpl_dens":         Union[float, None],
    "mpl_denserr1":     Union[float, None],
    "mpl_denserr2":     Union[float, None],
    "mpl_denslim":      Union[int, None],
    "ra_str":           Union[str, None],
    "dec_str":          Union[str, None],
    "mst_teff":         Union[float, None],
    "mst_tefferr1":     Union[float, None],
    "mst_tefferr2":     Union[float, None],
    "mst_tefflim":      Union[int, None],
    "mst_mass":         Union[float, None],
    "mst_masserr1":     Union[float, None],
    "mst_masserr2":     Union[float, None],
    "mst_masslim":      Union[int, None],
    "mst_rad":          Union[float, None],
    "mst_raderr1":      Union[float, None],
    "mst_raderr2":      Union[float, None],
    "mst_radlim":       Union[int, None],
    "rowupdate":        Union[str, None],
}


class ExoplanetExtendedData(object):
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
    def from_dict(cls, data: dict) -> "ExoplanetExtendedData":
        return cls(data)


def _add_func(name: str):
    @property
    def fn(self) -> _ATTRS.get(name):
        if name not in self._cache:
            self._cache[name] = self._data.get(name)
        return self._cache[name]
    setattr(ExoplanetExtendedData, name, fn)


for attr in _ATTRS:
    _add_func(attr)
