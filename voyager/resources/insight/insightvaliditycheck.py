from typing import Generator, List, Union
from .atmospherictemperature import AtmosphericTemperature
from .horizontalwindspeed import HorizontalWindSpeed
from .pressuredata import PressureData
from .winddirection import WindDirection


_ATTRS = {
    'atmospheric_temperature': ("AT", AtmosphericTemperature),
    'horizontal_wind_speed': ("HWS", HorizontalWindSpeed),
    'pressure_data': ("PRE", PressureData),
    'wind_direction': ("WD", WindDirection),
}


class InsightSolValidityCheck(object):
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
    def from_dict(cls, data: dict) -> "InsightSolValidityCheck":
        return cls(data)


class InsightValidityCheck(object):
    __slots__ = [
        '_sol_hrs',
        '_sols_checked',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict) -> None:
        self._sol_hrs = data.get("sol_hours_required")
        self._sols_checked = data.get("sols_checked")
        self._data = data

    def __iter__(self):
        return self

    def __next__(self):
        for sol in self.checks:
            yield sol

    @property
    def sol_hours_required(self) -> int:
        return self._sol_hrs

    @property
    def required_hours(self) -> int:
        return self.sol_hours_required

    @property
    def sols_checked(self) -> List[int]:
        return [int(sol) for sol in self._sols_checked]

    def _process_checks(self) -> Union[Generator[InsightSolValidityCheck, None, None], InsightSolValidityCheck, None]:
        if not (sol := self.sols_checked):
            return None
        elif len(sol) != 1:
            return (InsightSolValidityCheck(self._data.get(str(sl))) for sl in sol)
        else:
            return InsightSolValidityCheck(self._data.get(sol[0]))

    @property
    def checks(self) -> Union[Generator[InsightSolValidityCheck, None, None], InsightSolValidityCheck, None]:
        if (ck := f"{self}checks") not in self._cache:
            self._cache[ck] = self._process_checks()
        return self._cache[ck]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "InsightValidityCheck":
        return cls(data)


def _add_func(name: str, abbrev: str, _class: object):
    @property
    def fn(self) -> _class:
        if (c := name) not in self._cache:
            self._cache[c] = _class(self._data.get(abbrev))
        return self._cache[c]
    setattr(InsightSolValidityCheck, name, fn)


for attr, abbrevclass in _ATTRS.items():
    _add_func(attr, *abbrevclass)
