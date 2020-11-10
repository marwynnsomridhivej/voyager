from typing import Union


_ATTRS = {
    "star_id":         Union[int, None],
    "targettype":      Union[str, None],
    "field":           Union[str, None],
    "quarter":         Union[int, None],
    "ra":              Union[float, None],
    "dec":             Union[float, None],
    "pm_ra":           Union[float, None],
    "pm_dec":          Union[float, None],
    "pm_total":        Union[float, None],
    "gal_lat":         Union[float, None],
    "gal_lon":         Union[float, None],
    "start_time":      Union[float, None],
    "end_time":        Union[float, None],
    "umag":            Union[float, None],
    "gmag":            Union[float, None],
    "rmag":            Union[float, None],
    "imag":            Union[float, None],
    "zmag":            Union[float, None],
    "gredmag":         Union[float, None],
    "d51mag":          Union[float, None],
    "jmag":            Union[float, None],
    "hmag":            Union[float, None],
    "kmag":            Union[float, None],
    "kepmag":          Union[float, None],
    "filter":          Union[str, None],
    "npts":            Union[int, None],
    "gkcolor":         Union[float, None],
    "grcolor":         Union[float, None],
    "jkcolor":         Union[float, None],
    "reddening":       Union[float, None],
    "extinction":      Union[float, None],
    "eff_temp":        Union[int, None],
    "surface_gravity": Union[float, None],
    "metallicity":     Union[float, None],
    "radius":          Union[float, None],
    "object_status":   Union[int, None],
    "file_version":    Union[float, None],
    "data_release":    Union[int, None],
    "exposure":        Union[float, None],
    "livetime":        Union[float, None],
    "cdpp3_0":         Union[float, None],
    "cdpp6_0":         Union[float, None],
    "cdpp12_0":        Union[float, None],
    "crowdsap":        Union[float, None],
    "flfrcsap":        Union[float, None],
    "pdcmethod":       Union[str, None],
    "pdcvar":          Union[float, None],
    "pdc_tot":         Union[float, None],
    "pdc_totp":        Union[float, None],
    "pdc_cor":         Union[float, None],
    "pdc_corp":        Union[float, None],
    "pdc_var":         Union[float, None],
    "pdc_varp":        Union[float, None],
    "pdc_noi":         Union[float, None],
    "pdc_noip":        Union[float, None],
    "pdc_ept":         Union[float, None],
    "pdc_eptp":        Union[float, None],
}


class KeplerTimeSeries(object):
    __slots__ = [
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "KeplerTimeSeries":
        return cls(data)


def _add_func(name: str):
    @property
    def fn(self) -> _ATTRS.get(name):
        return self._data.get(name)
    setattr(KeplerTimeSeries, name, fn)


for attr in _ATTRS:
    _add_func(attr)
