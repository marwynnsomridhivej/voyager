import datetime
from asyncio.events import AbstractEventLoop
from typing import Any, List, Union

from .base import BaseResource

__all__ = [
    'CMEResource',
]


class CMEImpact(object):
    __slots__ = [
        '_glancing',
        '_location',
        '_arrival_time',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict) -> None:
        self._glancing = data.get("isGlancingBlow")
        self._location = data.get("location")
        self._arrival_time = data.get("arrivalTime")
        self._data = data

    @property
    def is_glancing_blow(self) -> bool:
        return self._glancing

    @property
    def location(self) -> str:
        return self._location

    @property
    def arrival_time(self) -> str:
        return self._arrival_time

    def _process_arrival(self) -> datetime.datetime:  # TODO: Implement datetime.datetime version
        return

    @property
    def arrival_datetime(self) -> datetime.datetime:
        if self not in self._cache:
            self._cache[self] = self._process_arrival()
        return self._cache[self]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "CMEImpact":
        return cls(data)


class CMEEnlilList(object):
    __slots__ = [
        '_model_comp_time',
        '_au',
        '_est_shock_arrival',
        '_est_duration',
        '_rmin_re',
        '_kp_18',
        '_kp_90',
        '_kp_135',
        '_kp_180',
        '_is_earth_gb',
        '_link',
        '_data'
    ]
    _cache = {}

    def __init__(self, data: dict) -> None:
        self._model_comp_time = data.get("modelCompletionTime")
        self._au = data.get("au")
        self._est_shock_arrival = data.get("estimatedShockArrivalTime")
        self._est_duration = data.get("estimatedDuration")
        self._rmin_re = data.get("rmin_re")
        self._kp_18 = data.get("kp_18")
        self._kp_90 = data.get("kp_90")
        self._kp_135 = data.get("kp_135")
        self._kp_180 = data.get("kp_180")
        self._is_earth_gb = data.get("isEarthGB")
        self._link = data.get("link")
        self._impact_list = data.get("impactList")
        self._data = data

    def _process_impacts(self) -> Union[List[CMEImpact], CMEImpact, None]:
        if not (data := self._data.get("impactList")):
            return None
        elif len(data) != 1:
            return [CMEImpact(subdata) for subdata in data]
        else:
            return CMEImpact(data[0])

    @property
    def impact_list(self) -> Union[List[CMEImpact], CMEImpact, None]:
        if (imp := f"{self}impacts") not in self._cache:
            self._cache[imp] = self._process_impacts()
        return self._cache[imp]

    def _process_ids(self) -> Union[List[str], str, None]:
        if not (data := self._data.get("cmdIDs")):
            return None
        if len(data) != 1:
            return [item for item in data]
        else:
            return data[0]

    @property
    def cme_ids(self) -> Union[List[str], str, None]:
        if (ids := f"{self}ids") not in self._cache:
            self._cache[ids] = self._process_ids()
        return self._cache[ids]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "CMEEnlilList":
        return cls(data)


class CMEAnalysis(object):
    __slots__ = [
        '_time21_5',
        '_latitude',
        '_longitude',
        '_half_angle',
        '_speed',
        '_type',
        '_is_most_accurate',
        '_associatedCMEID',
        '_note',
        '_catalog',
        '_level_of_data',
        '_link',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict) -> None:
        self._time21_5 = data.get("time21_5")
        self._latitude = data.get("latitude")
        self._longitude = data.get("longitude")
        self._half_angle = data.get("halfAngle")
        self._speed = data.get("speed")
        self._type = data.get("type")
        self._is_most_accurate = data.get("isMostAccurate")
        self._associatedCMEID = data.get("associatedCMEID")
        self._note = data.get("note")
        self._catalog = data.get("catalog")
        self._level_of_data = data.get("levelOfData")
        self._link = data.get("link")
        self._data = data

    @property
    def time21_5(self) -> str:  # TODO: Implement datetime.datetime version
        return self._time21_5

    @property
    def latitude(self) -> float:
        return self._latitude

    @property
    def longitude(self) -> float:
        return self._longitude

    @property
    def half_angle(self) -> float:
        return self._half_angle

    @property
    def speed(self) -> float:
        return self._speed

    @property
    def type(self) -> str:
        return self._type

    @property
    def is_most_accurate(self) -> bool:
        return self._is_most_accurate

    @property
    def associatedCMEID(self) -> Union[str, None]:
        return self._associatedCMEID

    @property
    def note(self) -> str:
        return self._note

    @property
    def catalog(self) -> Union[str, None]:
        return self._catalog

    @property
    def level_of_data(self) -> int:
        return self._level_of_data

    @property
    def link(self) -> str:
        return self._link

    def _process_enlil(self) -> Union[List[CMEEnlilList], CMEEnlilList, None]:
        if not (enlil := self._data.get("enlilList")):
            return None
        elif len(enlil) != 1:
            return [CMEEnlilList(data) for data in enlil]
        else:
            return CMEEnlilList(enlil[0])

    @property
    def enlillist(self) -> Union[List[CMEEnlilList], CMEEnlilList, None]:
        if self not in self._cache:
            self._cache[self] = self._process_enlil()
        return self._cache[self]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "CMEAnalysis":
        return cls(data)


class CMEInstrument(object):
    __slots__ = [
        '_id',
        '_display_name',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._id = data.get("id")
        self._display_name = data.get("displayName")
        self._data = data

    @property
    def id(self) -> int:
        return self._id

    @property
    def display_name(self) -> str:
        return self._display_name

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "CMEInstrument":
        return cls(data)


class CMEResource(BaseResource):
    __slots__ = [
        '_activity_id',
        '_catalog',
        '_start_time',
        '_source_location',
        '_active_region_num',
        '_link',
        '_note',
        '_linked_events',
        '_data'
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(CMEResource, self).__init__(data, loop=loop)
        self._activity_id = data.get("activityID")
        self._catalog = data.get("catalog")
        self._start_time = data.get("startTime")
        self._source_location = data.get("sourceLocation")
        self._active_region_num = data.get("activeRegionNum")
        self._link = data.get("link")
        self._note = data.get("note")
        self._linked_events = data.get("linkedEvents")
        self._data = data

    @property
    def activity_id(self) -> str:
        return self._activity_id

    @property
    def catalog(self) -> str:
        return self._catalog

    @property
    def start_time(self) -> str:  # TODO: Add datetime return
        return self._start_time

    @property
    def source_location(self) -> str:
        return self._source_location

    @property
    def active_region_num(self) -> Union[Any, None]:
        return self._active_region_num

    @property
    def link(self) -> str:
        return self._link

    @property
    def note(self) -> str:
        return self._note

    @property
    def linked_events(self) -> Union[List[Any], None]:
        return self._linked_events

    def _process_instruments(self) -> Union[List[CMEInstrument], CMEInstrument, None]:
        if not (instrs := self._data.get("instruments")):
            return None
        elif len(instrs) != 1:
            return [CMEInstrument(data) for data in instrs]
        else:
            return CMEInstrument(instrs[0])

    @property
    def instruments(self) -> Union[List[CMEInstrument], CMEInstrument, None]:
        if (instr := f"{self}instr") not in self._cache:
            self._cache[instr] = self._process_instruments()
        return self._cache[instr]

    def _process_analyses(self) -> Union[List[CMEAnalysis], CMEAnalysis, None]:
        if not (cme := self._data.get("cmeAnalyses")):
            return None
        elif len(cme) != 1:
            return [CMEAnalysis(data) for data in cme]
        else:
            return CMEAnalysis(cme[0])

    @property
    def cme_analyses(self) -> Union[List[CMEAnalysis], CMEAnalysis, None]:
        if (cme := f"{self}cme") not in self._cache:
            self._cache[cme] = self._process_analyses()
        return self._cache[cme]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "CMEResource":
        return cls(data, loop=loop)


class CMEAnalysisResource(BaseResource):
    __slots__ = [
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(CMEAnalysisResource, self).__init__(data, loop=loop)
        self._data = data

    def _process_analyses(self) -> Union[List[CMEAnalysis], CMEAnalysis, None]:
        if not (ays := self._data):
            return None
        elif len(ays) != 1:
            return [CMEAnalysis(data) for data in ays]
        else:
            return CMEAnalysis(ays[0])

    @property
    def analyses(self) -> Union[List[CMEAnalysis], CMEAnalysis, None]:
        if self not in self._cache:
            self._cache[self] = self._process_analyses()
        return self._cache[self]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "CMEAnalysisResource":
        return cls(data, loop=loop)
