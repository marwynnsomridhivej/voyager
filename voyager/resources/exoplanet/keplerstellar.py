from typing import Union


_ATTRS = {
    "st_delivname":    Union[str, None],
    "kepid":           Union[int, None],
    "tm_designation":  Union[str, None],
    "ra":              Union[float, None],
    "dec":             Union[float, None],
    "kepmag":          Union[float, None],
    "teff":            Union[int, None],
    "teff_err1":       Union[float, None],
    "teff_err2":       Union[float, None],
    "teff_prov":       Union[str, None],
    "logg":            Union[float, None],
    "logg_err1":       Union[float, None],
    "logg_err2":       Union[float, None],
    "logg_prov":       Union[str, None],
    "feh":             Union[float, None],
    "feh_err1":        Union[float, None],
    "feh_err2":        Union[float, None],
    "feh_prov":        Union[str, None],
    "radius":          Union[float, None],
    "radius_err1":     Union[float, None],
    "radius_err2":     Union[float, None],
    "mass":            Union[float, None],
    "mass_err1":       Union[float, None],
    "mass_err2":       Union[float, None],
    "dens":            Union[float, None],
    "dens_err1":       Union[float, None],
    "dens_err2":       Union[float, None],
    "prov_sec":        Union[float, None],
    "nconfp":          Union[int, None],
    "nkoi":            Union[int, None],
    "ntce":            Union[int, None],
    "st_quarters":     Union[float, None],
    "st_vet_date_str": Union[str, None],
}


class KeplerStellar(object):
    __slots__ = [
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "KeplerStellar":
        return cls(data)


def _add_func(name: str):
    @property
    def fn(self) -> _ATTRS.get(name):
        return self._data.get(name)
    setattr(KeplerStellar, name, fn)


for attr in _ATTRS:
    _add_func(attr)
