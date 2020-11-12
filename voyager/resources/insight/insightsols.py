from .atmospherictemperature import AtmosphericTemperature
from .horizontalwindspeed import HorizontalWindSpeed
from .pressuredata import PressureData
from .winddirection import WindDirection


class InsightSol(object):
    __slots__ = [
        '_first_utc',
        '_last_utc',
        '_season',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict) -> None:
        self._first_utc = data.get("First_UTC")
        self._last_utc = data.get("Last_UTC")
        self._season = data.get("Season")
        self._data = data

    @property
    def first_utc(self) -> str:
        return self._first_utc

    @property
    def last_utc(self) -> str:
        return self._last_utc

    @property
    def season(self) -> str:
        return self._season

    @property
    def atmospheric_temperature(self) -> AtmosphericTemperature:
        if (at := f"{self}at") not in self._cache:
            self._cache[at] = AtmosphericTemperature(self._data.get("AT"))
        return self._cache[at]

    @property
    def horizontal_wind_speed(self) -> HorizontalWindSpeed:
        if (hws := f"{self}hws") not in self._cache:
            self._cache[hws] = HorizontalWindSpeed(self._data.get("HWS"))
        return self._cache[hws]

    @property
    def pressure_data(self) -> PressureData:
        if (pre := f"{self}pre") not in self._cache:
            self._cache[pre] = PressureData(self._data.get("PRE"))
        return self._cache[pre]

    @property
    def wind_direction(self) -> WindDirection:
        if (wd := f"{self}wd") not in self._cache:
            self._cache[wd] = WindDirection(self._data.get("WD"))
        return self._cache[wd]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "InsightSol":
        return cls(data)
