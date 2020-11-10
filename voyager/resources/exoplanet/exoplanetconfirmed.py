from typing import Union


_ATTRS = {
    "pl_hostname":     Union[str, None],
    "pl_letter":       Union[str, None],
    "pl_name":         Union[str, None],
    "pl_discmethod":   Union[str, None],
    "pl_controvflag":  Union[int, None],
    "pl_pnum":         Union[int, None],
    "pl_orbper":       Union[float, None],
    "pl_orbpererr1":   Union[float, None],
    "pl_orbpererr2":   Union[float, None],
    "pl_orbperlim":    Union[int, None],
    "pl_orbpern":      Union[int, None],
    "pl_orbsmax":      Union[float, None],
    "pl_orbsmaxerr1":  Union[float, None],
    "pl_orbsmaxerr2":  Union[float, None],
    "pl_orbsmaxlim":   Union[int, None],
    "pl_orbsmaxn":     Union[int, None],
    "pl_orbeccen":     Union[float, None],
    "pl_orbeccenerr1": Union[float, None],
    "pl_orbeccenerr2": Union[float, None],
    "pl_orbeccenlim":  Union[int, None],
    "pl_orbeccenn":    Union[int, None],
    "pl_orbincl":      Union[float, None],
    "pl_orbinclerr1":  Union[float, None],
    "pl_orbinclerr2":  Union[float, None],
    "pl_orbincllim":   Union[int, None],
    "pl_orbincln":     Union[int, None],
    "pl_bmassj":       Union[float, None],
    "pl_bmassjerr1":   Union[float, None],
    "pl_bmassjerr2":   Union[float, None],
    "pl_bmassjlim":    Union[int, None],
    "pl_bmassn":       Union[int, None],
    "pl_bmassprov":    Union[str, None],
    "pl_radj":         Union[float, None],
    "pl_radjerr1":     Union[float, None],
    "pl_radjerr2":     Union[float, None],
    "pl_radjlim":      Union[int, None],
    "pl_radn":         Union[int, None],
    "pl_dens":         Union[float, None],
    "pl_denserr1":     Union[float, None],
    "pl_denserr2":     Union[float, None],
    "pl_denslim":      Union[int, None],
    "pl_densn":        Union[int, None],
    "pl_ttvflag":      Union[int, None],
    "pl_kepflag":      Union[int, None],
    "pl_k2flag":       Union[int, None],
    "ra_str":          Union[str, None],
    "dec_str":         Union[str, None],
    "ra":              Union[float, None],
    "st_raerr":        Union[float, None],
    "dec":             Union[float, None],
    "st_decerr":       Union[float, None],
    "st_posn":         Union[int, None],
    "st_dist":         Union[float, None],
    "st_disterr1":     Union[float, None],
    "st_disterr2":     Union[float, None],
    "st_distlim":      Union[int, None],
    "st_distn":        Union[int, None],
    "st_optmag":       Union[float, None],
    "st_optmagerr":    Union[float, None],
    "st_optmaglim":    Union[int, None],
    "st_optband":      Union[str, None],
    "gaia_gmag":       Union[float, None],
    "gaia_gmagerr":    Union[float, None],
    "gaia_gmaglim":    Union[int, None],
    "st_teff":         Union[float, None],
    "st_tefferr1":     Union[float, None],
    "st_tefferr2":     Union[float, None],
    "st_tefflim":      Union[int, None],
    "st_teffn":        Union[int, None],
    "st_mass":         Union[float, None],
    "st_masserr1":     Union[float, None],
    "st_masserr2":     Union[float, None],
    "st_masslim":      Union[int, None],
    "st_massn":        Union[int, None],
    "st_rad":          Union[float, None],
    "st_raderr1":      Union[float, None],
    "st_raderr2":      Union[float, None],
    "st_radlim":       Union[int, None],
    "st_radn":         Union[int, None],
    "pl_nnotes":       Union[int, None],
    "rowupdate":       Union[str, None],
    "pl_facility":     Union[str, None],
}


class ConfirmedExoplanetData(object):
    __slots__ = [
        '_data'
    ]
    _cache = {}

    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "ConfirmedExoplanetData":
        return cls(data)


def _add_func(name: str):
    @property
    def fn(self) -> _ATTRS.get(name):
        if name not in self._cache:
            self._cache[name] = self._data.get(name)
        return self._cache[name]
    setattr(ConfirmedExoplanetData, name, fn)


for attr in _ATTRS:
    _add_func(attr)
