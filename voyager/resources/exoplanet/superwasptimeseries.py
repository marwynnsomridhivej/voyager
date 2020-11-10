from typing import Union


_ATTRS = {
    "sourceid":        Union[str, None],
    "hjdstart":        Union[float, None],
    "hjdstop":         Union[float, None],
    "hjd_ref":         Union[float, None],
    "obsstart":        Union[str, None],
    "obsstop":         Union[str, None],
    "tstart":          Union[int, None],
    "tstop":           Union[int, None],
    "ra":              Union[float, None],
    "dec":             Union[float, None],
    "wasp_mag":        Union[float, None],
    "npts":            Union[int, None],
    "tile":            Union[str, None],
    "tm_statnpts":     Union[int, None],
    "tm_median":       Union[float, None],
    "tm_stddevwrtmed": Union[float, None],
    "tm_range595":     Union[float, None],
}


class SuperWASPTimeSeries(object):
    __slots__ = [
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "SuperWASPTimeSeries":
        return cls(data)


def _add_func(name: str):
    @property
    def fn(self) -> _ATTRS.get(name):
        return self._data.get(name)
    setattr(SuperWASPTimeSeries, name, fn)


for attr in _ATTRS:
    _add_func(attr)
