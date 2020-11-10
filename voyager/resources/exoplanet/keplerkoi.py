from typing import Union

_ATTRS = {
    "kepid":             Union[int, None],
    "kepoi_name":        Union[str, None],
    "kepler_name":       Union[str, None],
    "koi_disposition":   Union[str, None],
    "koi_pdisposition":  Union[str, None],
    "koi_score":         Union[float, None],
    "koi_fpflag_nt":     Union[int, None],
    "koi_fpflag_ss":     Union[int, None],
    "koi_fpflag_co":     Union[int, None],
    "koi_fpflag_ec":     Union[int, None],
    "koi_period":        Union[float, None],
    "koi_period_err1":   Union[float, None],
    "koi_period_err2":   Union[float, None],
    "koi_time0bk":       Union[float, None],
    "koi_time0bk_err1":  Union[float, None],
    "koi_time0bk_err2":  Union[float, None],
    "koi_impact":        Union[float, None],
    "koi_impact_err1":   Union[float, None],
    "koi_impact_err2":   Union[float, None],
    "koi_duration":      Union[float, None],
    "koi_duration_err1": Union[float, None],
    "koi_duration_err2": Union[float, None],
    "koi_depth":         Union[float, None],
    "koi_depth_err1":    Union[float, None],
    "koi_depth_err2":    Union[float, None],
    "koi_prad":          Union[float, None],
    "koi_prad_err1":     Union[float, None],
    "koi_prad_err2":     Union[float, None],
    "koi_teq":           Union[float, None],
    "koi_teq_err1":      Union[float, None],
    "koi_teq_err2":      Union[float, None],
    "koi_insol":         Union[float, None],
    "koi_insol_err1":    Union[float, None],
    "koi_insol_err2":    Union[float, None],
    "koi_model_snr":     Union[float, None],
    "koi_tce_plnt_num":  Union[int, None],
    "koi_tce_delivname": Union[str, None],
    "koi_steff":         Union[float, None],
    "koi_steff_err1":    Union[float, None],
    "koi_steff_err2":    Union[float, None],
    "koi_slogg":         Union[float, None],
    "koi_slogg_err1":    Union[float, None],
    "koi_slogg_err2":    Union[float, None],
    "koi_srad":          Union[float, None],
    "koi_srad_err1":     Union[float, None],
    "koi_srad_err2":     Union[float, None],
    "ra_str":            Union[str, None],
    "dec_str":           Union[str, None],
    "koi_kepmag":        Union[float, None],
    "koi_kepmag_err":    Union[float, None],
}


class KeplerKOI(object):
    __slots__ = [
        '_data'
    ]

    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "KeplerKOI":
        return cls(data)


def _add_func(name: str):
    @property
    def fn(self) -> _ATTRS.get(name):
        return self._data.get(name)
    setattr(KeplerKOI, name, fn)


for attr in _ATTRS:
    _add_func(attr)
