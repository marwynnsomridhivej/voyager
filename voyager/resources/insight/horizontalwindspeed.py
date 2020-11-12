from typing import List, Union


class HorizontalWindSpeed(object):
    __slots__ = [
        '_av',
        '_ct',
        '_mn',
        '_mx',
        '_sol_hrs',
        '_valid',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._av = data.get("av")
        self._ct = data.get("ct")
        self._mn = data.get("mn")
        self._mx = data.get("mx")
        self._sol_hrs = data.get("sol_hours_with_data")
        self._valid = data.get("valid")
        self._data = data

    @property
    def av(self) -> float:
        return self._av

    @property
    def ct(self) -> float:
        return self._ct

    @property
    def mn(self) -> float:
        return self._mn

    @property
    def mx(self) -> float:
        return self._mx

    @property
    def sol_hours_with_data(self) -> List[int]:
        return self._sol_hrs

    @property
    def valid(self) -> Union[bool, None]:
        return self._valid

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "HorizontalWindSpeed":
        return cls(data)
