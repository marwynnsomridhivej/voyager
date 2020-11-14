from typing import Union


__all__ = [
    'MissionDesignObject',
]


def _handle_int(pot_int: str) -> Union[int, str]:
    try:
        return int(pot_int)
    except ValueError:
        return pot_int


class MissionDesignObject(object):
    __slots__ = [
        '_data_arc',
        '_md_orbit_id',
        '_orbit_class',
        '_spkid',
        '_condition_code',
        '_orbit_id',
        '_fullname',
        '_des',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._data_arc = _handle_int(data.get("data_arc"))
        self._md_orbit_id = _handle_int(data.get("md_orbit_id"))
        self._orbit_class = data.get("orbit_class")
        self._spkid = _handle_int(data.get("spkid"))
        self._condition_code = _handle_int(data.get("condition_code"))
        self._orbit_id = _handle_int(data.get("orbit_id"))
        self._fullname = data.get("fullname")
        self._des = data.get('des')
        self._data = data

    @property
    def data_arc(self) -> Union[int, str]:
        return self._data_arc

    @property
    def md_orbit_id(self) -> Union[int, str]:
        return self._md_orbit_id

    @property
    def orbit_class(self) -> str:
        return self._orbit_class

    @property
    def spkid(self) -> Union[int, str]:
        return self._spkid

    @property
    def condition_code(self) -> Union[int, str]:
        return self.condition_code

    @property
    def orbit_id(self) -> Union[int, str]:
        return self._orbit_id

    @property
    def fullname(self) -> str:
        return self._fullname

    @property
    def des(self) -> str:
        return self._des

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "MissionDesignObject":
        return cls(data)
