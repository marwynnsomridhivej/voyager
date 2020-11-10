from asyncio.events import AbstractEventLoop
from typing import Any, Generator, Union

from .base import BaseResource
from .exoplanet import *


__all__ = [
    'ExoplanetResource',
]

_TYPES = {
    'exoplanets': ExoplanetConfirmedData,
    'compositepars': ExoplanetCompositeData,
    'exomultpars': ExoplanetExtendedData,
    'aliastable': ExoplanetAlias,
    'microlensing': ExoplanetMicrolensing,
    'cumulative': KeplerKOI,
    'q1_q17_dr25_sup_koi': KeplerKOI,
    'q1_q17_dr25_koi': KeplerKOI,
    'q1_q17_dr24_koi': KeplerKOI,
    'q1_q16_koi': KeplerKOI,
    'q1_q12_koi': KeplerKOI,
    'q1_q8_koi': KeplerKOI,
    'q1_q6_koi': KeplerKOI,
    'q1_q17_dr25_tce': ThresholdCrossingEvent,
    'q1_q17_dr24_tce': ThresholdCrossingEvent,
    'q1_q16_tce': ThresholdCrossingEvent,
    'q1_q12_tce': ThresholdCrossingEvent,
    'keplerstellar': KeplerStellar,
    'q1_q17_dr25_supp_stellar': KeplerStellar,
    'q1_q17_dr25_stellar': KeplerStellar,
    'q1_q17_dr24_stellar': KeplerStellar,
    'q1_q16_stellar': KeplerStellar,
    'q1_q12_stellar': KeplerStellar,
    'keplertimeseries': KeplerTimeSeries,
    'keplernames': KeplerNames,
    'kelttimeseries': KELTTimeSeries,
    'kelt': KELTTimeSeries,
    'superwasptimeseries': SuperWASPTimeSeries,
    'k2targets': K2Target,
    'k2candidates': K2Candidate,
    'k2names': K2Name,
    'missionstars': MissionStars,
    'mission_exocat': MissionStars,
}


class ExoplanetResource(BaseResource):
    __slots__ = [
        '_table_name',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(ExoplanetResource, self).__init__(data, loop=loop)
        self._table_name = data.get("table_name")
        self._data = data.get("raw")

    def __iter__(self):
        return self

    def __next__(self):
        for res in self.results:
            yield res

    def _process_results(self) -> Union[Generator[Any, None, None], Any, None]:
        _class = _TYPES.get(self._table_name)
        if not (res := self._data):
            return None
        elif len(res) != 1:
            return (_class(data) for data in res)
        else:
            return _class(res[0])

    @property
    def results(self) -> Union[Generator[Any, None, None], Any, None]:
        if self not in self._cache:
            self._cache[self] = self._process_results()
        return self._cache[self]

    @property
    def table_name(self) -> str:
        return self._table_name

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "ExoplanetResource":
        return cls(data, loop=loop)
