__all__ = [
    'MissionDesignDVLowThrust',
]


class MissionDesignDVLowThrust(object):
    __slots__ = [
        '_sep',
        '_const',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._sep = data.get("sep")
        self._const = data.get("const")
        self._data = data

    @property
    def sep(self) -> float:
        return self._sep

    @property
    def const(self) -> float:
        return self._const

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "MissionDesignDVLowThrust":
        return cls(data)
