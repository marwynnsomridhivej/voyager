from typing import Union


_ATTRS = {
    "kepid":            Union[int, None],
    "tce_plnt_num":     Union[int, None],
    "tce_rogue_flag":   Union[int, None],
    "tce_period":       Union[float, None],
    "tce_period_err":   Union[float, None],
    "tce_time0bk":      Union[float, None],
    "tce_time0bk_err":  Union[float, None],
    "tce_impact":       Union[float, None],
    "tce_impact_err":   Union[float, None],
    "tce_duration":     Union[float, None],
    "tce_duration_err": Union[float, None],
    "tce_depth":        Union[float, None],
    "tce_depth_err":    Union[float, None],
    "tce_model_snr":    Union[float, None],
    "tce_prad":         Union[float, None],
    "tce_prad_err":     Union[float, None],
    "tce_eqt":          Union[float, None],
    "tce_eqt_err":      Union[float, None],
    "tce_insol":        Union[float, None],
    "tce_insol_err":    Union[float, None],
    "tce_steff":        Union[float, None],
    "tce_steff_err":    Union[float, None],
    "tce_slogg":        Union[float, None],
    "tce_slogg_err":    Union[float, None],
    "tce_sradius":      Union[float, None],
    "tce_sradius_err":  Union[float, None],
}


class ThresholdCrossingEvent(object):
    __slots__ = [
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "ThresholdCrossingEvent":
        return cls(data)


def _add_func(name: str):
    @property
    def fn(self) -> _ATTRS.get(name):
        return self._data.get(name)
    setattr(ThresholdCrossingEvent, name, fn)


for attr in _ATTRS:
    _add_func(attr)
