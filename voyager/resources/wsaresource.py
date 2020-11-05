from asyncio.events import AbstractEventLoop
from typing import List, Union

from .base import BaseResource


__all__ = [
    'WSAResource'
]


class WSAInstrument(object):
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
    def from_dict(cls, data: dict) -> "WSAInstrument":
        return cls(data)


class WSAIPList(object):
    __slots__ = [
        '_catalog',
        '_activity_id',
        '_location',
        '_event_time',
        '_link',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict) -> None:
        self._catalog = data.get("catalog")
        self._activity_id = data.get("activity_id")
        self._location = data.get("location")
        self._event_time = data.get("eventTime")
        self._link = data.get("link")
        self._data = data

    @property
    def catalog(self) -> str:
        return self._catalog

    @property
    def activity_id(self) -> str:
        return self._activity_id

    @property
    def id(self) -> str:
        return self.activity_id

    @property
    def location(self) -> str:
        return self._location

    @property
    def event_time(self) -> str:  # TODO: Implement datetime.datetime
        return self._event_time

    @property
    def link(self) -> str:
        return self._link

    def _process_instruments(self) -> Union[List[WSAInstrument], WSAInstrument, None]:
        if not (instrs := self._data.get("instruments")):
            return None
        elif len(instrs) != 1:
            return [WSAInstrument(data) for data in instrs]
        else:
            return WSAInstrument(instrs[0])

    @property
    def instruments(self) -> Union[List[WSAInstrument], WSAInstrument, None]:
        if self not in self._cache:
            self._cache[self] = self._process_instruments()
        return self._cache[self]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "WSAIPList":
        return cls(data)


class WSAEnlil(object):
    __slots__ = [
        '_start_time',
        '_latitude',
        '_longitude',
        '_speed',
        '_half_angle',
        '_time21_5',
        '_is_most_accurate',
        '_level_of_data',
        '_cme_id',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict) -> None:
        self._start_time = data.get("cmeStartTime")
        self._latitude = data.get("latitude")
        self._longitude = data.get("longitude")
        self._speed = data.get("speed")
        self._half_angle = data.get("halfAngle")
        self._time21_5 = data.get("time21_5")
        self._is_most_accurate = data.get("isMostAccurate")
        self._level_of_data = data.get("levelOfData")
        self._cme_id = data.get("cmeid")
        self._data = data

    @property
    def start_time(self) -> str:  # TODO: Implement datetime.datetime
        return self._start_time

    @property
    def latitude(self) -> float:
        return self._latitude

    @property
    def longitude(self) -> float:
        return self._longitude

    @property
    def speed(self) -> float:
        return self._speed

    @property
    def half_angle(self) -> float:
        return self._half_angle

    @property
    def time21_5(self) -> str:  # TODO: Implement datetime.datetime
        return self._time21_5

    @property
    def is_most_accurate(self) -> bool:
        return self._is_most_accurate

    @property
    def level_of_data(self) -> int:
        return self._level_of_data

    def _process_ips_list(self) -> Union[List[WSAIPList], WSAIPList, None]:
        if not (ips := self._data.get("ipsList")):
            return None
        elif len(ips) != 1:
            return [WSAIPList(data) for data in ips]
        else:
            return WSAIPList(ips[0])

    @property
    def ips_list(self) -> Union[List[WSAIPList], WSAIPList, None]:
        if self not in self._cache:
            self._cache[self] = self._process_ips_list()
        return self._cache[self]

    @property
    def cme_id(self) -> str:
        return self._cme_id

    @property
    def id(self) -> str:
        return self.cme_id

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "WSAEnlil":
        return cls(data)


class WSAImpact(object):
    __slots__ = [
        '_glancing',
        '_location',
        '_arrival_time',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._glancing = data.get("isGlancingBlow")
        self._location = data.get("location")
        self._arrival_time = data.get("arrivalTime")
        self._data = data

    @property
    def is_glancing_blow(self) -> bool:
        return self._glancing

    @property
    def glancing(self) -> bool:
        return self.is_glancing_blow

    @property
    def location(self) -> str:
        return self._location

    @property
    def arrival_time(self) -> str:  # TODO: Implement datetime.datetime
        return self._arrival_time

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "WSAImpact":
        return cls(data)


class WSAResource(BaseResource):
    __slots__ = [
        '_simulation_id',
        '_model_completion_time',
        '_au',
        '_est_shock_arrival_time',
        '_est_duration',
        '_rmin_re',
        '_kp_18',
        '_kp_90',
        '_kp_135',
        '_kp_180',
        '_is_earth_gb',
        '_link',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(WSAResource, self).__init__(data, loop=loop)
        self._simulation_id = data.get("simulationID")
        self._model_completion_time = data.get("modelCompletionTime")
        self._au = data.get("au")
        self._est_shock_arrival_time = data.get("estimatedShockArrivalTime")
        self._est_duration = data.get("estimatedDuration")
        self._rmin_re = data.get("rmin_re")
        self._kp_18 = data.get("kp_18")
        self._kp_90 = data.get("kp_90")
        self._kp_135 = data.get("kp_135")
        self._kp_180 = data.get("kp_180")
        self._is_earth_gb = data.get("isEarthGB")
        self._link = data.get("link")
        self._data = data

    @property
    def simulation_id(self) -> str:
        return self._simulation_id

    @property
    def id(self) -> str:
        return self.simulation_id

    @property
    def model_completion_time(self) -> str:  # TODO: Implement datetime.datetime
        return self._model_completion_time

    @property
    def au(self) -> float:
        return self._au

    def _process_cme_inputs(self) -> Union[List[WSAEnlil], WSAEnlil, None]:
        if not (cme := self._data.get("cmeInputs")):
            return None
        elif len(cme) != 1:
            return [WSAEnlil(data) for data in cme]
        else:
            return WSAEnlil(cme[0])

    @property
    def cme_inputs(self) -> Union[List[WSAEnlil], WSAEnlil, None]:
        if (cme := f"{self}inputs") not in self._cache:
            self._cache[cme] = self._process_cme_inputs()
        return self._cache[cme]

    @property
    def estimated_shock_arrival_time(self) -> str:  # TODO: Implement datetime.datetime
        return self._est_shock_arrival_time

    @property
    def est_shock_arrival_time(self) -> str:
        return self.estimated_shock_arrival_time

    @property
    def estimated_duration(self) -> str:  # TODO: Implement datetime.timedelta
        return self._est_duration

    @property
    def est_duration(self) -> str:
        return self.estimated_duration

    @property
    def rmin_re(self) -> str:
        return self._rmin_re

    @property
    def kp_18(self) -> str:
        return self._kp_18

    @property
    def kp_90(self) -> str:
        return self._kp_90

    @property
    def kp_139(self) -> str:
        return self._kp_135

    @property
    def kp_180(self) -> str:
        return self._kp_180

    @property
    def is_earth_gb(self) -> bool:
        return self._is_earth_gb

    @property
    def isEarthGB(self) -> bool:
        return self.is_earth_gb

    def _process_impact_list(self) -> Union[List[WSAImpact], WSAImpact, None]:
        if not (il := self._data.get("impactList")):
            return None
        elif len(il) != 1:
            return [WSAImpact(data) for data in il]
        else:
            return WSAImpact(il[0])

    @property
    def impact_list(self) -> Union[List[WSAImpact], WSAImpact, None]:
        if (il := f"{self}impact") not in self._cache:
            self._cache[il] = self._process_impact_list()
        return self._cache[il]

    @property
    def link(self) -> str:
        return self._link

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "WSAResource":
        return cls(data, loop=loop)
