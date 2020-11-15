from asyncio.events import AbstractEventLoop
from collections import namedtuple
from typing import Union

from ..base import BaseResource

_ATTRS = {
    "min_size": int,
    "occ": int,
    "n_via_traj": int,
    "size": Union[int, None],
    "size_sigma": Union[int, None],
    "radar_snr_a": float,
    "obs_mag": float,
    "orbit_id": int,
    "h": float,
    "obs_flag": Union[str, None],
    "obs_end": str,
    "radar_snr_g": int,
    "radar_obs_a": str,
    "obs_start": str,
    "radar_obs_g": str,
    "computer": Union[str, None],
    "fullname": str,
    "des": str,
    "max_size": int,
}
_TRAJATTRS = {
    "c3": float,
    "vrel_arr_earth": float,
    "dur_total": int,
    "dv_total": float,
    "tid": int,
    "vrel_arr_neo": float,
    "v_dep_earth": float,
    "vrel_dep_neo": float,
    "dur_at": int,
    "launch": str,
    "dec_arr": float,
    "dv_dep_park": float,
    "dur_out": int,
    "dur_ret": int,
    "v_arr_earth": float,
    "dec_dep": float,
}
_DUR = namedtuple("TrajectoryRecord", ["dv", "dur"])


def _handle(pot_num: str) -> Union[float, int, str]:
    try:
        if "." in pot_num:
            return float(pot_num)
        else:
            return int(pot_num)
    except ValueError:
        return pot_num


class NHATTrajectory(object):
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
    def from_dict(cls, data: dict) -> "NHATTrajectory":
        return cls(data)


class NHATSData(BaseResource):
    __slots__ = [
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(NHATSData, self).__init__(data, loop=loop)
        self._data = data

    @property
    def min_dv(self) -> namedtuple:
        return _DUR(*self._data.get("min_dv"))

    @property
    def min_dv_traj(self) -> NHATTrajectory:
        if (mdvt := f"{self}mindivtraj") not in self._cache:
            self._cache[mdvt] = NHATTrajectory(self._data.get("min_dv_traj"))
        return self._cache[mdvt]

    @property
    def min_dur(self) -> namedtuple:
        return _DUR(*self._data.get("min_dur"))

    @property
    def min_dur_traj(self) -> NHATTrajectory:
        if (mdrt := f"{self}mindurtraj") not in self._cache:
            self._cache[mdrt] = NHATTrajectory(self._data.get("min_dur_traj"))
        return self._cache[mdrt]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "NHATSData":
        return cls(data)


def _add_func(_class, attr_ref, name: str):
    @property
    def fn(self) -> attr_ref.get(name):
        if name not in self._cache:
            self._cache[name] = _handle(self._data.get(name))
        return self._cache[name]
    setattr(_class, name, fn)


for attr in _ATTRS:
    _add_func(NHATSData, _ATTRS, attr)


for attr in _TRAJATTRS:
    _add_func(NHATTrajectory, _TRAJATTRS, attr)
