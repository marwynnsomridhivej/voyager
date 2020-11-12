from typing import Union


class CompassPoint(object):
    __slots__ = [
        '_degrees',
        '_point',
        '_right',
        '_up',
        '_ct',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._degrees = data.get("compass_degrees")
        self._point = data.get("compass_point")
        self._right = data.get("compass_right")
        self._up = data.get("compass_up")
        self._ct = data.get("ct")
        self._data = data

    @property
    def compass_degrees(self) -> float:
        return self._degrees

    @property
    def degrees(self) -> float:
        return self.compass_degrees

    @property
    def compass_point(self) -> str:
        return self._point

    @property
    def point(self) -> str:
        return self.compass_point

    @property
    def compass_right(self) -> float:
        return self._right

    @property
    def right(self) -> float:
        return self.compass_right

    @property
    def compass_up(self) -> float:
        return self._up

    @property
    def up(self) -> float:
        return self.compass_up

    @property
    def ct(self) -> int:
        return self._ct

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "CompassPoint":
        return cls(data)


class WindDirection(object):
    __slots__ = [
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def most_common(self) -> Union[CompassPoint, None]:
        if (n := "mc") not in self._cache:
            self._cache[n] = CompassPoint(data) if (
                data := self._data.get("most_common")
            ) else None
        return self._cache[n]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "WindDirection":
        return cls(data)


def _add_func(number: int):
    @property
    def fn(self) -> Union[CompassPoint, None]:
        if (n := str(number)) not in self._cache:
            self._cache[n] = CompassPoint(data) if (
                data := self._data.get(str(number))
            ) else None
        return self._cache[n]
    setattr(WindDirection, f"point{number + 1}", fn)


for num in range(0, 15):
    _add_func(num)
