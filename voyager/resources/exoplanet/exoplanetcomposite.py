from typing import Union


_ATTRS = {
    "fpl_hostname":      Union[str, None],
    "fpl_letter":        Union[str, None],
    "fpl_name":          Union[str, None],
    "fpl_discmethod":    Union[str, None],
    "fpl_disc":          Union[int, None],
    "fpl_controvflag":   Union[int, None],
    "fpl_orbper":        Union[float, None],
    "fpl_orbpererr1":    Union[float, None],
    "fpl_orbpererr2":    Union[float, None],
    "fpl_orbperlim":     Union[int, None],
    "fpl_orbperreflink": Union[str, None],
    "fpl_smax":          Union[float, None],
    "fpl_smaxerr1":      Union[float, None],
    "fpl_smaxerr2":      Union[float, None],
    "fpl_smaxlim":       Union[int, None],
    "fpl_smaxreflink":   Union[str, None],
    "fpl_eccen":         Union[float, None],
    "fpl_eccenerr1":     Union[float, None],
    "fpl_eccenerr2":     Union[float, None],
    "fpl_eccenlim":      Union[int, None],
    "fpl_eccenreflink":  Union[str, None],
    "fpl_bmasse":        Union[float, None],
    "fpl_bmasseerr1":    Union[float, None],
    "fpl_bmasseerr2":    Union[float, None],
    "fpl_bmasselim":     Union[int, None],
    "fpl_bmassprov":     Union[str, None],
    "fpl_bmassreflink":  Union[str, None],
    "fpl_rade":          Union[float, None],
    "fpl_radeerr1":      Union[float, None],
    "fpl_radeerr2":      Union[float, None],
    "fpl_radelim":       Union[int, None],
    "fpl_radreflink":    Union[str, None],
    "fpl_dens":          Union[float, None],
    "fpl_denserr1":      Union[float, None],
    "fpl_denserr2":      Union[float, None],
    "fpl_denslim":       Union[int, None],
    "fpl_densreflink":   Union[str, None],
    "fpl_eqt":           Union[float, None],
    "fpl_eqterr1":       Union[float, None],
    "fpl_eqterr2":       Union[float, None],
    "fpl_eqtlim":        Union[int, None],
    "fpl_eqtreflink":    Union[str, None],
    "fpl_insol":         Union[float, None],
    "fpl_insolerr1":     Union[float, None],
    "fpl_insolerr2":     Union[float, None],
    "fpl_insollim":      Union[int, None],
    "fpl_insolreflink":  Union[str, None],
    "ra_str":            Union[str, None],
    "dec_str":           Union[str, None],
    "fst_posreflink":    Union[str, None],
    "fst_dist":          Union[float, None],
    "fst_disterr1":      Union[float, None],
    "fst_disterr2":      Union[float, None],
    "fst_distlim":       Union[int, None],
    "fst_distreflink":   Union[str, None],
    "fst_optmag":        Union[float, None],
    "fst_optmagerr":     Union[float, None],
    "fst_optmaglim":     Union[int, None],
    "fst_optmagband":    Union[str, None],
    "fst_optmagreflink": Union[str, None],
    "fst_nirmag":        Union[float, None],
    "fst_nirmagerr":     Union[float, None],
    "fst_nirmaglim":     Union[int, None],
    "fst_nirmagband":    Union[str, None],
    "fst_nirmagreflink": Union[str, None],
    "fst_spt":           Union[float, None],
    "fst_sptlim":        Union[int, None],
    "fst_sptreflink":    Union[str, None],
    "fst_teff":          Union[float, None],
    "fst_tefferr1":      Union[float, None],
    "fst_tefferr2":      Union[float, None],
    "fst_tefflim":       Union[int, None],
    "fst_teffreflink":   Union[str, None],
    "fst_logg":          Union[float, None],
    "fst_loggerr1":      Union[float, None],
    "fst_loggerr2":      Union[float, None],
    "fst_logglim":       Union[int, None],
    "fst_loggreflink":   Union[str, None],
    "fst_lum":           Union[float, None],
    "fst_lumerr1":       Union[float, None],
    "fst_lumerr2":       Union[float, None],
    "fst_lumlim":        Union[int, None],
    "fst_lumreflink":    Union[str, None],
    "fst_mass":          Union[float, None],
    "fst_masserr1":      Union[float, None],
    "fst_masserr2":      Union[float, None],
    "fst_masslim":       Union[int, None],
    "fst_massreflink":   Union[str, None],
    "fst_rad":           Union[float, None],
    "fst_raderr1":       Union[float, None],
    "fst_raderr2":       Union[float, None],
    "fst_radlim":        Union[int, None],
    "fst_radreflink":    Union[str, None],
    "fst_met":           Union[float, None],
    "fst_meterr1":       Union[float, None],
    "fst_meterr2":       Union[float, None],
    "fst_metlim":        Union[int, None],
    "fst_metratio":      Union[str, None],
    "fst_metreflink":    Union[str, None],
    "fst_age":           Union[float, None],
    "fst_ageerr1":       Union[float, None],
    "fst_ageerr2":       Union[float, None],
    "fst_agelim":        Union[int, None],
    "fst_agereflink":    Union[str, None],
}


class ExoplanetCompositeData(object):
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
    def from_dict(cls, data: dict) -> "ExoplanetCompositeData":
        return cls(data)


def _add_func(name: str):
    @property
    def fn(self) -> _ATTRS.get(name):
        return self._data.get(name)
    setattr(ExoplanetCompositeData, name, fn)


for attr in _ATTRS:
    _add_func(attr)
