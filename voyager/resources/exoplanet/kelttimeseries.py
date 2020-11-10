from typing import Union


_ATTRS = {
    "kelt_sourceid":     Union[str, None],
    "kelt_field":        Union[str, None],
    "kelt_orientation":  Union[str, None],
    "proc_type":         Union[str, None],
    "kelt_proc_version": Union[str, None],
    "ra":                Union[float, None],
    "dec":               Union[float, None],
    "kelt_mag":          Union[float, None],
    "obsstart":          Union[str, None],
    "obsstop":           Union[str, None],
    "bjdstart":          Union[float, None],
    "bjdstop":           Union[float, None],
    "mean":              Union[float, None],
    "stddevwrtmean":     Union[float, None],
    "median":            Union[float, None],
    "stddevwrtmedian":   Union[float, None],
    "npts":              Union[int, None],
    "n5sigma":           Union[int, None],
    "f5sigma":           Union[float, None],
    "medabsdev":         Union[float, None],
    "chisquared":        Union[float, None],
    "range595":          Union[float, None],
    "minvalue":          Union[float, None],
    "maxvalue":          Union[float, None],
}


class KELTTimeSeries(object):
    __slots__ = [
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "KELTTimeSeries":
        return cls(data)


def _add_func(name: str):
    @property
    def fn(self) -> _ATTRS.get(name):
        return self._data.get(name)
    setattr(KELTTimeSeries, name, fn)


for attr in _ATTRS:
    _add_func(attr)
